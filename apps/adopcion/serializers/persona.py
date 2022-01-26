# DRF modules
from rest_framework import serializers
# Local modules - Models
from apps.adopcion.models import Persona


class PersonaSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        return super(PersonaSerializer).update(instance, validated_data)

    def create(self, validated_data):
        return super(PersonaSerializer).update(validated_data)

    class Meta:
        model = Persona
        fields = '__all__'


class EditPersonaSerializer(serializers.Serializer):
    nombre = serializers.CharField(
        max_length=50,
        trim_whitespace=True
    )
    apellidos = serializers.CharField(
        max_length=70,
        trim_whitespace=True
    )
    edad = serializers.IntegerField(
        min_value=10,
        max_value=150
    )
    telefono = serializers.CharField(
        required=False,
        min_length=8,
        max_length=12,
        trim_whitespace=True
    )
    email = serializers.EmailField(
        max_length=150,
        trim_whitespace=True
    )
    domicilio = serializers.CharField(
        required=False,
        max_length=255
    )

    def create(self, data):
        return Persona.objects.create(**data)

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.apellidos = validated_data.get('apellidos', instance.apellidos)
        instance.edad = validated_data.get('edad', instance.edad)
        instance.telefono = validated_data.get('telefono', instance.telefono)
        instance.email = validated_data.get('email', instance.email)
        instance.domicilio = validated_data.get('domicilio', instance.domicilio)
        instance.save()
        return instance