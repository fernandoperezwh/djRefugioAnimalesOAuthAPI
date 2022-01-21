# DRF modules
from rest_framework import serializers
# Local modules - Models
from app.mascota.models import Mascota


class MascotaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mascota
        fields = ['nombre', 'sexo', 'edad_aproximada', 'fecha_rescate']
