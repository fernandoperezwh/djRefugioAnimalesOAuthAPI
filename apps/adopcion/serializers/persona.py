# DRF modules
from rest_framework import serializers
# Local modules - Models
from apps.adopcion.models import Persona


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'
