from django.db import models

# Create your models here.

class Faccion(models.Model):
    nombre = models.CharField(max_length=100)