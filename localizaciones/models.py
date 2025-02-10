from django.db import models

class Localizacion(models.Model):
    """Modelo para representar una localización en el juego."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre