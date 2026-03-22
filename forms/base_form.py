from utils import constants


class BaseForm:
    def __init__(self):
        self.base_speed = constants.BASE_SPEED
        self.color = constants.BLUE
        self.base_jump_force = constants.BASE_JUMP_FORCE
        self.base_health = constants.BASE_PLAYER_HEALTH
        self.base_attack = constants.BASE_PLAYER_ATTACK
        self.base_defense = constants.BASE_PLAYER_DEFENSE


    def apply(self, player):
        player.speed = self.base_speed
        player.color = self.color
        player.jump_force = self.base_jump_force
        player.health = self.base_health
        player.defense = self.base_defense
        player.attack = self.base_attack
        player.can_fly = False



