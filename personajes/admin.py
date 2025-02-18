from django.contrib import admin
from django.utils.html import format_html
from .models import Personaje, Inventario, InventarioItem
from equipamiento.models import Arma, Armadura, Consumible


class InventarioItemInline(admin.TabularInline):
    model = InventarioItem
    extra = 1


@admin.register(Personaje)
class PersonajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'faccion', 'localizacion', 'mostrar_imagen')
    list_filter = ('faccion', 'localizacion')
    search_fields = ('nombre',)

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" />', obj.imagen.url)
        return "Sin imagen"

    mostrar_imagen.short_description = 'Imagen'


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('personaje',)
    inlines = [InventarioItemInline]


@admin.register(InventarioItem)
class InventarioItemAdmin(admin.ModelAdmin):
    list_display = ('inventario', 'get_item_name', 'cantidad')

    def get_item_name(self, obj):
        if isinstance(obj.item, Arma):
            return obj.item.nombre
        elif isinstance(obj.item, Armadura):
            return obj.item.nombre
        elif isinstance(obj.item, Consumible):
            return obj.item.tipo
        return "Sin nombre"

    get_item_name.short_description = 'Item'