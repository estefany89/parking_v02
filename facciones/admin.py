from django.contrib import admin
from .models import Faccion

@admin.register(Faccion)
class FaccionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre', 'descripcion')