from django.contrib import admin
from .models import Localizacion

@admin.register(Localizacion)
class LocalizacionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre', 'descripcion')