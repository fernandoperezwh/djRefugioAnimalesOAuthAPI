# DRF modules
from rest_framework import serializers
# Local modules - Models
from apps.mascota.models import Vacuna


class VacunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacuna
        fields = '__all__'
