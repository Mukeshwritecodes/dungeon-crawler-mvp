from forms.base_form import BaseForm
from utils import constants


class BatForm(BaseForm):
    def apply(self, player):
        multiplier = [3, 0.5]
        player.speed = self.base_speed * multiplier[0]
        player.jump_force = self.base_jump_force * multiplier[1]
        player.color = constants.RED
        player.is_flying = True
        #player.defense += 2
