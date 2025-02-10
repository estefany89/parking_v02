from django.contrib import admin

from equipamiento.models import Ataque, Arma, Armadura, Consumible, ItemInstancia


class AtaqueInline(admin.TabularInline):
    """Permite gestionar ataques dentro del admin de armas."""
    model = Ataque
    extra = 1
    min_num = 1
    max_num = 4


@admin.register(Arma)
class ArmaAdmin(admin.ModelAdmin):
    """Admin para gestionar armas con ataques en línea."""
    list_display = ("nombre", "tipo", "dano_base", "es_unica")
    search_fields = ("nombre", "tipo")
    list_filter = ("tipo", "es_unica")
    inlines = [AtaqueInline]

    def save_model(self, request, obj, form, change):
        """Valida que solo haya una arma única en el juego."""
        if obj.es_unica and Arma.objects.filter(es_unica=True).exclude(pk=obj.pk).exists():
            from django.core.exceptions import ValidationError
            raise ValidationError("Solo puede existir una arma única en todo el juego.")
        super().save_model(request, obj, form, change)


@admin.register(Armadura)
class ArmaduraAdmin(admin.ModelAdmin):
    """Admin para gestionar armaduras."""
    list_display = ("nombre", "defensa_fisica", "defensa_magica")
    search_fields = ("nombre",)


@admin.register(Consumible)
class ConsumibleAdmin(admin.ModelAdmin):
    """Admin para gestionar consumibles."""
    list_display = ("tipo", "potencia")
    search_fields = ("tipo",)


@admin.register(ItemInstancia)
class ItemInstanciaAdmin(admin.ModelAdmin):
    """Admin para gestionar instancias de ítems."""
    list_display = ("item", "content_type", "object_id")
    search_fields = ("item",)
    list_filter = ("content_type",)