from django.contrib import admin
# local imports
from apps.adopcion.models import Persona


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "apellidos",
        "edad",
        "telefono",
        "email",
        "domicilio",
    )
    list_filter = ( "nombre", "apellidos", )
    ordering = ("-nombre", "-apellidos", )