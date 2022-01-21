# DRF modules
from rest_framework import serializers
# Local modules - Models
from app.mascota.models import Vacuna


class VacunaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vacuna
