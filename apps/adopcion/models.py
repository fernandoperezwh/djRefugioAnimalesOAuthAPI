from django.db import models


class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=70)
    edad = models.IntegerField()
    telefono = models.CharField(max_length=12)
    email = models.EmailField()
    domicilio = models.TextField()

    def __str__(self):
        return "{} {}".format(self.nombre, self.apellidos)
