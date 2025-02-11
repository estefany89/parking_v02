from django.db import models
from django.dispatch import receiver
from equipamiento.models import Arma, Armadura, ItemInstancia
from facciones.models import Faccion
from localizaciones.models import Localizacion
from PIL import Image


class Personaje(models.Model):
    nombre = models.CharField(max_length=100)
    localizacion = models.ForeignKey(Localizacion, on_delete=models.SET_NULL, null=True)
    faccion = models.ForeignKey(Faccion, on_delete=models.SET_NULL, null=True)
    arma_equipada = models.ForeignKey(Arma, on_delete=models.SET_NULL, null=True, blank=True)
    armadura_equipada = models.ForeignKey(Armadura, on_delete=models.SET_NULL, null=True, blank=True)
    imagen = models.ImageField(upload_to='personajes/', null=True, blank=True, default='personajes/default.jpg')

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
        if self.inventario.items.filter(item_instancia=arma).exists():
            self.arma_equipada = arma
            self.save()

    def equipar_armadura(self, armadura):
        """Equipa una armadura si el personaje la tiene en su inventario."""
        if self.inventario.items.filter(item_instancia=armadura).exists():
            self.armadura_equipada = armadura
            self.save()

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


class Inventario(models.Model):
    personaje = models.OneToOneField(Personaje, on_delete=models.CASCADE, related_name="inventario")

    def __str__(self):
        return f"Inventario de {self.personaje.nombre}"


class InventarioItem(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name="items")
    item_instancia = models.OneToOneField(ItemInstancia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item_instancia} en {self.inventario.personaje.nombre}"
