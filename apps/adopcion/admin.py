from django.contrib import admin
# local imports
from apps.mascota.models import  Mascota, Vacuna



@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "sexo",
        "edad",
        "foto",
        "fecha_rescate",
        "persona",
        # "vacunas",
    )
    list_filter = ( "nombre", "fecha_rescate", )
    ordering = ("-fecha_rescate", )
    date_hierarchy = "fecha_rescate"


@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
    )
    list_filter = ( "nombre", )
