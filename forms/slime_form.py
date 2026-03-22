from forms.base_form import BaseForm
from utils import constants


class SlimeForm(BaseForm):

    def apply(self, player):

        multiplier = {
            "speed": 0.5,
            "jump_force": 0.5,
            "health": 1,
            "defense": 1.5,
            "attack": 2
        }

        player.speed = self.base_speed * multiplier["speed"]
        player.jump_force = self.base_jump_force * multiplier["jump_force"]
        player.health = self.base_health * multiplier["health"]
        player.defense = self.base_defense * multiplier["defense"]
        player.attack = self.base_attack * multiplier["attack"]
        player.can_fly = False

