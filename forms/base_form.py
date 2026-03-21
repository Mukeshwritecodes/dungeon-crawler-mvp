from utils import constants


class BaseForm:
    def __init__(self):
        self.base_speed = constants.BASE_SPEED
        self.color = constants.BLUE
        self.base_jump_force = constants.BASE_JUMP_FORCE


    def apply(self, player):
        player.speed = self.base_speed
        player.color = self.color
        player.jump_force = self.base_jump_force
        player.is_flying = False
        #player.damage += 1



