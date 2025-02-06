from django.db import models

# Create your models here.

class Personaje(models.Model):
    nombre = models.CharField(max_length=100)

class Inventario(models.Model):
    pass

class InventarioItem(models.Model):
    pass