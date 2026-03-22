from forms.base_form import BaseForm
from utils import constants


class BatForm(BaseForm):
    def apply(self, player):

        multiplier = {
            "speed": 2,
            "jump_force": 0.5,
            "health": 0.75,
            "defense": 0.75,
            "attack": 1.5
        }

        player.speed = self.base_speed * multiplier["speed"]
        player.jump_force = self.base_jump_force * multiplier["jump_force"]
        player.health = self.base_health * multiplier["health"]
        player.defense = self.base_defense * multiplier["defense"]
        player.attack = self.base_attack * multiplier["attack"]
        player.can_fly = True
