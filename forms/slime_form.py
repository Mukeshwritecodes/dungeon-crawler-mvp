from forms.base_form import BaseForm
from utils import constants


class SlimeForm(BaseForm):
    def apply(self, player):
        multiplier = 0.5
        player.speed = self.base_speed * multiplier
        player.color = constants.GREEN
        #player.damage += 5


