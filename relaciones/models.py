from django.db import models

from personajes.models import Personaje


# Create your models here.

class Relacion(models.Model):
    AMIGOS = "A"
    ENEMIGOS = "E"
    NEUTRALES = "N"
    TIPOS_RELACIONES = [
        (AMIGOS, "Amigos"),
        (ENEMIGOS, "Enemigos"),
        (NEUTRALES, "Neutrales"),
    ]
    personaje1 = models.ForeignKey(Personaje, related_name='personaje1', on_delete=models.CASCADE)
    personaje2 = models.ForeignKey(Personaje, related_name='personaje2', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS_RELACIONES)