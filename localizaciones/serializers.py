from rest_framework import serializers
from .models import Localizacion

class LocalizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localizacion
        fields = ["id", "nombre", "descripcion"]