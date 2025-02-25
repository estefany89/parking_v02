from django.db import models

class Faccion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(default="Sin información conocida")
    def __str__(self):
        return self.nombre