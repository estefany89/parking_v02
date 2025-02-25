from rest_framework import serializers
from .models import Personaje

class PersonajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personaje
        fields = ['id', 'nombre', 'hp', 'localizacion', 'faccion', 'arma_equipada', 'armadura_equipada', 'imagen']

    arma_equipada = serializers.StringRelatedField(allow_null=True)
    armadura_equipada = serializers.StringRelatedField(allow_null=True)
    localizacion = serializers.StringRelatedField(allow_null=True)
    faccion = serializers.StringRelatedField(allow_null=True)