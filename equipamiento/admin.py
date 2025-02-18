from django.contrib import admin
from .models import Arma, Ataque, Armadura, Consumible

class AtaqueInline(admin.TabularInline):
    model = Ataque
    extra = 1
    max_num = 4

@admin.register(Arma)
class ArmaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'dano_base', 'es_unica')
    list_filter = ('tipo', 'es_unica')
    search_fields = ('nombre',)
    inlines = [AtaqueInline]

@admin.register(Ataque)
class AtaqueAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'arma', 'dano')
    list_filter = ('arma',)
    search_fields = ('nombre', 'arma__nombre')

@admin.register(Armadura)
class ArmaduraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'defensa')
    search_fields = ('nombre',)

@admin.register(Consumible)
class ConsumibleAdmin(admin.ModelAdmin):
    list_display = ('get_tipo_display', 'potencia')
    list_filter = ('tipo',)