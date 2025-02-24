from django.contrib.contenttypes.models import ContentType
from django.db import models
from equipamiento.models import Arma, Armadura, Consumible
from facciones.models import Faccion
from localizaciones.models import Localizacion
from PIL import Image
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey


class Personaje(models.Model):
    nombre = models.CharField(max_length=100)
    localizacion = models.ForeignKey(Localizacion, on_delete=models.SET_NULL, null=True)
    faccion = models.ForeignKey(Faccion, on_delete=models.SET_NULL, null=True)
    arma_equipada = models.ForeignKey(Arma, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    armadura_equipada = models.ForeignKey(Armadura, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    imagen = models.ImageField(upload_to='personajes/', null=True, blank=True, default='personajes/default.jpg')
    hp = models.IntegerField(default=100)

    def save(self, *args, **kwargs):
        """Redimensiona la imagen antes de guardar el personaje."""
        super().save(*args, **kwargs)  # Guarda el personaje primero para obtener un ID

        if self.imagen:
            self.redimensionar_imagen()


    def redimensionar_imagen(self, size=(300, 300)):
        """Redimensiona la imagen a 300x300 px asegurando compatibilidad de formato."""
        try:
            imagen_path = self.imagen.path
            with Image.open(imagen_path) as imagen:
                imagen = imagen.convert("RGB")  # Convertir a RGB para evitar errores
                imagen = imagen.resize(size, Image.Resampling.LANCZOS)
                imagen.save(imagen_path, format="JPEG", quality=90)
        except Exception as e:
            print(f"Error al redimensionar la imagen: {e}")

    def equipar_arma(self, arma):
        """Equipa un arma si el personaje la tiene en su inventario."""
        arma_ct = ContentType.objects.get_for_model(arma)
        if self.inventario.items.filter(content_type=arma_ct, object_id=arma.id).exists():
            self.arma_equipada = arma
            self.save()
        else:
            raise ValidationError("No puedes equipar un arma que no está en tu inventario")

    def equipar_armadura(self, armadura):
        """Equipa una armadura si el personaje la tiene en su inventario."""
        armadura_ct = ContentType.objects.get_for_model(armadura)
        if self.inventario.items.filter(content_type=armadura_ct, object_id=armadura.id).exists():
            self.armadura_equipada = armadura
            self.save()
        else:
            raise ValidationError("No puedes equipar una armadura que no está en tu inventario")

    def desequipar_arma(self):
        """Desequipa el arma actual."""
        self.arma_equipada = None
        self.save()

    def desequipar_armadura(self):
        """Desequipa la armadura actual."""
        self.armadura_equipada = None
        self.save()

    def __str__(self):
        return self.nombre


class InventarioItem(models.Model):
    inventario = models.ForeignKey('Inventario', on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    cantidad = models.PositiveIntegerField(default=1)

    def clean(self):
        """Validar que el item instanciado sea un arma, armadura o consumible."""
        if not isinstance(self.item, (Arma, Armadura, Consumible)):
            raise ValidationError("Solo puedes guardar armas, armaduras y consumibles en el inventario")

    def __str__(self):
        return f"{self.cantidad}x {self.item}"


class Inventario(models.Model):
    personaje = models.OneToOneField(Personaje, on_delete=models.CASCADE, related_name="inventario")

    def __str__(self):
        return f"Inventario de {self.personaje.nombre}"