import random


class BattleService:
    def __init__(self, player, machine):
        """
        Initialize the battle service with player and machine characters.

        Args:
            player: The player character
            machine: The machine character
        """
        self.player = player
        self.machine = machine
        self.initial_hp = 100

    def start_battle(self):
        """Initialize battle with atomic transaction to ensure data consistency"""
        self.player.hp = self.initial_hp
        self.machine.hp = self.initial_hp
        self.player.save()
        self.machine.save()

    def _calculate_damage(self, attack):
        """Calculate actual damage with some randomness"""
        base_damage = attack.dano
        return round(base_damage)

    def _apply_damage(self, target, damage):
        """Apply damage to target and ensure HP doesn't go below 0"""
        target.hp = max(0, target.hp - damage)
        target.save()


    def player_attack(self, attack):
        """
        Process player's attack and machine's counter-attack

        Args:
            attack: The attack being used by the player

        Returns:
            dict: Battle state after the attack
        """
        if not attack:
            raise ValueError("No attack specified")

        # Calculate and apply damage
        damage = self._calculate_damage(attack)
        self._apply_damage(self.machine, damage)

        battle_state = {
            'damage_dealt': damage,
            'attack_name': attack.nombre,
            'player_hp': self.player.hp,
            'machine_hp': self.machine.hp,
            'winner': None
        }

        # Check if machine is defeated
        if self.machine.hp <= 0:
            battle_state['winner'] = 'player'
            return battle_state

        # Machine counter-attack
        machine_result = self.machine_turn()
        battle_state.update(machine_result)

        return battle_state


    def machine_turn(self):
        """
        Process machine's turn

        Returns:
            dict: Battle state after machine's attack
        """
        available_attacks = self.machine.arma_equipada.ataques.all()
        if not available_attacks:
            raise ValueError("Machine has no available attacks")

        # Select random attack and calculate damage
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

        # Check if player is defeated
        if self.player.hp <= 0:
            battle_state['winner'] = 'machine'

        return battle_state