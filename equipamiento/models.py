from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.models import ContentType

class Arma(models.Model):
    TIPOS_ARMA = [
        ("espada", "Espada"),
        ("hacha", "Hacha"),
        ("daga", "Daga"),
        ("arco", "Arco"),
        ("baston", "Bastón"),
    ]
    nombre = models.CharField(max_length=100)
    dano_base = models.PositiveIntegerField()
    tipo = models.CharField(max_length=10, choices=TIPOS_ARMA)
    es_unica = models.BooleanField(default=False)

    def clean(self):
        """Si es un arma única, asegurarse de que solo haya una en el juego."""
        if self.es_unica and Arma.objects.filter(nombre=self.nombre, es_unica=True).exclude(pk=self.pk).exists():
            raise ValidationError("Solo puede existir una arma única en todo el juego.")

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class Ataque(models.Model):
    TIPOS_ATAQUE = [
        ("fisico", "Físico"),
        ("magico", "Mágico"),
    ]
    nombre = models.CharField(max_length=100)
    dano = models.PositiveIntegerField()
    tipo_ataque = models.CharField(max_length=10, choices=TIPOS_ATAQUE)
    arma = models.ForeignKey(Arma, on_delete=models.CASCADE, related_name="ataques")

    def __str__(self):
        return f"{self.nombre} - {self.tipo_ataque} ({self.dano} daño)"

    def clean(self):
        """Asegura que cada arma tenga entre 1 y 4 ataques."""
        if not (1 <= self.arma.ataques.count() <= 4):
            raise ValidationError("Cada arma debe tener entre 1 y 4 ataques.")


class Armadura(models.Model):
    nombre = models.CharField(max_length=100)
    defensa_fisica = models.PositiveIntegerField()
    defensa_magica = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

class Consumible(models.Model):
    TIPOS_CONSUMIBLE = [
        ("vida", "Poción de vida"),
        ("dano", "Poción de daño"),
    ]
    tipo = models.CharField(max_length=10, choices=TIPOS_CONSUMIBLE)
    potencia = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.get_tipo_display()} (+{self.potencia})"

class ItemInstancia(models.Model):
    """Modelo para manejar instancias de objetos en el juego usando GenericForeignKey."""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")

    def clean(self):
        """Validar que el item instanciado sea un arma, armadura o consumible."""
        if not isinstance(self.item, (Arma, Armadura, Consumible)):
            raise ValidationError("El objeto instanciado debe ser un arma, armadura o consumible.")

    def __str__(self):
        return f"Instancia de {self.item}"