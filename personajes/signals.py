from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Personaje, Inventario

@receiver(post_save, sender=Personaje)
def crear_inventario_automatico(sender, instance, created, **kwargs):
    """Crea automáticamente un inventario cuando se crea un personaje."""
    if created:  # Solo se ejecuta cuando se crea un nuevo personaje
        crear_inventario_automatico = Inventario.objects.create(personaje=instance)
        crear_inventario_automatico.save()