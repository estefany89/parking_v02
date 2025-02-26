import random


class BattleService:
    def __init__(self, player, machine):
        """
        Inicio el servicio con los personajes seleccionados y le asigno la vida inicial

        Args:
            player: Personaje del jugador
            machine: Personaje de la máquina
            initial_hp: Vida con la que comienzan el combate

        """
        self.player = player
        self.machine = machine
        self.initial_hp = 100

    def start_battle(self):
        """Guardo los personajes con la vida al 100% para comenzar la batalla"""
        self.player.hp = self.initial_hp
        self.machine.hp = self.initial_hp
        self.player.save()
        self.machine.save()

    def _calculate_damage(self, attack):
        """Calculo el daño del ataque redondeado"""
        base_damage = attack.dano + attack.arma.dano_base
        return round(base_damage)

    def _apply_damage(self, target, damage):
        """Aplico el daño a la vida del target, asegurando que no baje de 0"""
        target.hp = max(0, target.hp - damage)
        target.save()


    def player_attack(self, attack):
        """
        Procesa el ataque que selecciona el jugador y luego realiza un ataque aleatorio por parte de la máquina

        Args:
            attack: El ataque que usa el jugador

        Returns:
            dict: Estado de la batlla
        """
        if not attack:
            raise ValueError("Ningún ataque seleccionado")

        # Calculo y aplico el daño
        damage = self._calculate_damage(attack)
        self._apply_damage(self.machine, damage)

        battle_state = {
            'damage_dealt': damage,
            'attack_name': attack.nombre,
            'player_hp': self.player.hp,
            'machine_hp': self.machine.hp,
            'winner': None
        }

        # Miro si en el turno ha ganado el jugador
        if self.machine.hp <= 0:
            battle_state['winner'] = 'player'
            return battle_state

        # Si el jugador no ha ganado realizo el turno de la máquina
        machine_result = self.machine_turn()
        battle_state.update(machine_result)

        return battle_state


    def machine_turn(self):
        """
        Turno de la máquina donde selecciono un ataque aleatorio de los disponibles

        Returns:
            dict: Estado de la batalla al terminar el turno de la máquina
        """
        available_attacks = self.machine.arma_equipada.ataques.all()
        if not available_attacks:
            raise ValueError("La máquina no tiene ataques disponibles")

        # Selecciono un ataque aleatorio y aplico el daño
        attack = random.choice(available_attacks)
        damage = self._calculate_damage(attack)
        self._apply_damage(self.player, damage)

        battle_state = {
            'machine_damage_dealt': damage,
            'machine_attack_name': attack.nombre,
            'player_hp': self.player.hp,
            'machine_hp': self.machine.hp,
            'winner': None
        }

        # Miro si ha ganado la máquina
        if self.player.hp <= 0:
            battle_state['winner'] = 'machine'

        return battle_state