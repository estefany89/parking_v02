from django.contrib import admin
from .models import Relacion

@admin.register(Relacion)
class RelacionAdmin(admin.ModelAdmin):
    list_display = ('personaje1', 'personaje2', 'get_tipo_display')
    list_filter = ('tipo',)
    search_fields = ('personaje1__nombre', 'personaje2__nombre')