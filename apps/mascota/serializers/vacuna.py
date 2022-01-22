# DRF modules
from rest_framework import serializers
# Local modules - Models
from apps.mascota.models import Vacuna


class VacunaSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        return super(VacunaSerializer).update(instance, validated_data)

    def create(self, validated_data):
        return super(VacunaSerializer).update(validated_data)

    class Meta:
        model = Vacuna
        fields = '__all__'


class EditVacunaSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=50,trim_whitespace=True)

    def create(self, data):
        return Vacuna.objects.create(**data)

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.save()
        return instance