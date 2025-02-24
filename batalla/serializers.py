from rest_framework import serializers
from personajes.models import Personaje

class PersonajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personaje
        fields = ['id', 'nombre', 'hp', 'arma_equipada']

class BattleStateSerializer(serializers.Serializer):
    player_hp = serializers.FloatField()
    machine_hp = serializers.FloatField()
    winner = serializers.CharField(required=False)