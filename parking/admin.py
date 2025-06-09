from django.contrib import admin
from .models import Vehiculo, Parking, Plaza, RegistroOcupacion, PerfilUsuario

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'marca', 'modelo', 'color')

admin.site.register(Parking)
admin.site.register(Plaza)
admin.site.register(RegistroOcupacion)
admin.site.register(PerfilUsuario)