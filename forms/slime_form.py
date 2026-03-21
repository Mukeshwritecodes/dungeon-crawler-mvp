from forms.base_form import BaseForm
from utils import constants


class SlimeForm(BaseForm):
    def apply(self, player):
        multiplier = [0.5, 0.5]
        player.speed = self.base_speed * multiplier[0]
        player.jump_force = self.base_jump_force * multiplier[1]
        player.color = constants.GREEN
        player.is_flying = False
        #player.damage += 5


