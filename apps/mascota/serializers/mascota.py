# DRF packages
from rest_framework import serializers
# Local packages - Models
from rest_framework.exceptions import ValidationError

from apps.adopcion.models import Persona
from apps.mascota.models import Mascota, Vacuna
# local packages - serializers
from apps.adopcion.serializers import PersonaSerializer
from apps.mascota.serializers import VacunaSerializer


class MascotaSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(read_only=True)
    vacunas = VacunaSerializer(many=True, read_only=True)

    class Meta:
        model = Mascota
        fields = '__all__'


class EditMascotaSerializer(serializers.Serializer):
    nombre = serializers.CharField(
        max_length=50,
        trim_whitespace=True
    )
    sexo = serializers.CharField(
        max_length=10,
        trim_whitespace=True
    )
    edad = serializers.IntegerField(
        min_value=0,
        max_value=25
    )
    fecha_rescate = serializers.DateField()
    persona = serializers.IntegerField(write_only=True)
    vacunas = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def get_instance_persona(self, id):
        """
        Obtiene una instancia del modelo Persona en base al id
        :param id:
        :return:
        """
        try:
            return Persona.objects.get(pk=id)
        except Persona.DoesNotExist:
            raise ValidationError('Persona was not found')

    def get_instance_vacunas(self, list_ids):
        """
        Obtiene una lista de instancias del modelo Vacunas en base a la lista de ids
        :param ids:
        :return:
        """
        list_instance = Vacuna.objects.filter(id__in=list_ids)
        if not list_instance:
            raise ValidationError('Vacunas were not fount')
        return list_instance


    def create(self, data):
        # Se consultan las instancias de persona y vacunas por id
        persona_instance = self.get_instance_persona(data.pop('persona'))
        vacunas_instances = self.get_instance_vacunas(data.pop('vacunas'))
        # Se crea el registro de Mascota
        data['persona'] = persona_instance
        mascota_instance = Mascota.objects.create(**data)
        mascota_instance.vacunas.set(vacunas_instances)
        return mascota_instance

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.sexo = validated_data.get('sexo', instance.sexo)
        instance.edad = validated_data.get('edad', instance.edad)
        instance.fecha_rescate = validated_data.get('fecha_rescate', instance.fecha_rescate)
        instance.persona = self.get_instance_persona(validated_data.get('persona'))
        instance.vacunas = self.get_instance_vacunas(validated_data.get('vacunas'))
        instance.save()
        return instance
