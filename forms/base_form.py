from utils import constants


class BaseForm:
    def __init__(self):
        self.base_speed = constants.BASE_SPEED
        self.color = constants.BLUE

    def apply(self, player):
        player.speed = self.base_speed
        player.color = self.color
        #player.damage += 1

    def update(self, player, dt):
        pass

