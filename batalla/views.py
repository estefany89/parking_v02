from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from equipamiento.models import Ataque
from .forms import CharacterSelectionForm
from personajes.models import Personaje
from .services import BattleService


class CharacterSelectView(View):
    template_name = 'battle/character_select.html'
    form_class = CharacterSelectionForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form,
            'characters': Personaje.objects.all(),
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if not form.is_valid():
            messages.error(request, 'Por favor selecciona personajes válidos')
            return self.get(request)

        player = form.cleaned_data['player_character']
        machine = form.cleaned_data['machine_character']

        if player == machine:
            messages.error(request, 'Los personajes seleccionados deben ser diferentes')
            return self.get(request)

        return redirect('battle:start_battle', player_id=player.id, machine_id=machine.id)


class BattleView(View):
    template_name = 'battle/start_battle.html'

    def get(self, request, *args, **kwargs):
        try:
            player = Personaje.objects.get(id=kwargs['player_id'])
            machine = Personaje.objects.get(id=kwargs['machine_id'])

            # Obtener los ataques disponibles
            player_attacks = player.arma_equipada.ataques.all()
            machine_attacks = machine.arma_equipada.ataques.all()

        except ObjectDoesNotExist:
            messages.error(request, 'Personaje no encontrado')
            return redirect('battle:character_select')

        battle_service = BattleService(player, machine)
        battle_service.start_battle()

        context = {
            'player': player,
            'machine': machine,
            'player_attacks': player_attacks,
            'machine_attacks': machine_attacks,
            'winner': None,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            player = Personaje.objects.get(id=kwargs['player_id'])
            machine = Personaje.objects.get(id=kwargs['machine_id'])
            attack_id = request.POST.get('attack_id')

            if not attack_id:
                return JsonResponse({'error': 'No attack selected'}, status=400)

            # Obtener el ataque seleccionado
            attack = Ataque.objects.get(id=attack_id)

            # Verificar que el ataque pertenece al arma del jugador
            if attack not in player.arma_equipada.ataques.all():
                return JsonResponse({'error': 'Invalid attack'}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Character or attack not found'}, status=404)

        battle_service = BattleService(player, machine)
        result = battle_service.player_attack(attack)

        return JsonResponse(result)
