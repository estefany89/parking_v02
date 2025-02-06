from django.db import models

# Create your models here.

class Arma(models.Model):
    nombre = models.CharField(max_length=100)

class Ataque(models.Model):
    nombre = models.CharField(max_length=100)

class Armadura(models.Model):
    nombre = models.CharField(max_length=100)

class Consumible(models.Model):
    pass

class ItemInstancia(models.Model):
    pass