from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Personaje, Inventario, InventarioItem
from equipamiento.models import Arma, Armadura, ItemInstancia

class InventarioItemInline(admin.TabularInline):
    """Permite administrar los ítems del inventario directamente desde el personaje."""
    model = InventarioItem
    extra = 1


@admin.register(Personaje)
class PersonajeAdmin(admin.ModelAdmin):
    """Admin para gestionar personajes y validar equipamiento."""
    list_display = ("nombre", "localizacion", "faccion", "arma_equipada", "armadura_equipada")
    search_fields = ("nombre", "faccion__nombre", "localizacion__nombre")
    list_filter = ("faccion", "localizacion")
    inlines = [InventarioItemInline]

    def save_model(self, request, obj, form, change):
        """Valida que el personaje solo equipe armas o armaduras que tiene en su inventario."""
        errores = []

        # Validar que el arma equipada esté en el inventario del personaje
        if obj.arma_equipada:
            if not InventarioItem.objects.filter(
                inventario=obj.inventario,
                item_instancia__content_type__model="arma",
                item_instancia__object_id=obj.arma_equipada.id
            ).exists():
                errores.append(f"El personaje no tiene el arma {obj.arma_equipada} en su inventario.")

        # Validar que la armadura equipada esté en el inventario del personaje
        if obj.armadura_equipada:
            if not InventarioItem.objects.filter(
                inventario=obj.inventario,
                item_instancia__content_type__model="armadura",
                item_instancia__object_id=obj.armadura_equipada.id
            ).exists():
                errores.append(f"El personaje no tiene la armadura {obj.armadura_equipada} en su inventario.")

        # Si hay errores, lanzar una excepción ValidationError
        if errores:
            raise ValidationError(errores)

        super().save_model(request, obj, form, change)