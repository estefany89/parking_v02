from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Personaje, Inventario

@receiver(post_save, sender=Personaje)
def crear_inventario(sender, instance, created, **kwargs):
    if created:
        Inventario.objects.create(personaje=instance)