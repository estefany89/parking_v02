from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# -------------------------------
# Perfil de usuario (Admin / Operador)
# -------------------------------
class Parking(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    capacidad_total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"

    def plazas_libres(self):
        return self.plazas.filter(ocupada=False).count()

    def plazas_ocupadas(self):
        return self.plazas.filter(ocupada=True).count()

class PerfilUsuario(models.Model):
    ROLES = (
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True)
    rol = models.CharField(max_length=10, choices=ROLES)
    parkings = models.ManyToManyField(Parking, blank=True)  # Solo aplica a operadores

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"

# -------------------------------
# Plazas y vehículos
# -------------------------------
class Plaza(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='plazas')
    numero = models.CharField(max_length=10)
    ocupada = models.BooleanField(default=False)

    class Meta:
        unique_together = ['parking', 'numero']

    def __str__(self):
        estado = "Ocupada" if self.ocupada else "Libre"
        return f"Plaza {self.numero} - {self.parking.nombre} ({estado})"

class Vehiculo(models.Model):
    matricula = models.CharField(max_length=15, primary_key=True, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    propietario_nombre = models.CharField(max_length=100)
    propietario_telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.matricula} - {self.marca} {self.modelo} ({self.propietario_nombre})"

# -------------------------------
# Registro de ocupación
# -------------------------------
class RegistroOcupacion(models.Model):
    plaza = models.ForeignKey(Plaza, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_entrada = models.DateTimeField(default=timezone.now)  # Fecha y hora de entrada la actual por defecto
    fecha_salida = models.DateTimeField(null=True, blank=True)
    operador_entrada = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='entradas_registradas')
    operador_salida = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='salidas_registradas')

    class Meta:
        ordering = ['-fecha_entrada']

    def __str__(self):
        estado = "En parking" if not self.fecha_salida else "Finalizado"
        return f"{self.vehiculo.matricula} - Plaza {self.plaza.numero} ({estado})"

    def duracion(self):
        if self.fecha_salida:
            return self.fecha_salida - self.fecha_entrada
        return timezone.now() - self.fecha_entrada
