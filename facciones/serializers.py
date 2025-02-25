from rest_framework import serializers
from .models import Faccion

class FaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faccion
        fields = ["id", "nombre", "descripcion"]