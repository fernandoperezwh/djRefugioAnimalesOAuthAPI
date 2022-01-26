from django.db import models
#local imports
from apps.adopcion.models import Persona


class Vacuna(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    nombre = models.CharField(max_length=50)
    sexo = models.CharField(max_length=10)
    edad = models.IntegerField()
    foto = models.ImageField(upload_to="mascotas", null=True, blank=True)
    fecha_rescate = models.DateField()
    persona = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)
    vacunas = models.ManyToManyField(Vacuna)
    def __str__(self):
        return self.nombre
