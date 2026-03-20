from forms.base_form import BaseForm
from utils import constants


class BatForm(BaseForm):
    def apply(self, player):
        multiplier = 3
        player.speed = self.base_speed * multiplier
        player.color = constants.RED
        #player.defense += 2
