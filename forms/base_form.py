from utils import constants
from utils.helpers import Helper


class BaseForm:
    def __init__(self):
        self.base_speed = constants.BASE_SPEED
        self.color = constants.BLUE
        self.base_jump_force = constants.BASE_JUMP_FORCE
        self.base_health = constants.BASE_PLAYER_HEALTH
        self.base_attack = constants.BASE_PLAYER_ATTACK
        self.base_defense = constants.BASE_PLAYER_DEFENSE

        helper = Helper()

        self.running_right = helper.load_sprites("assets/sprites/player-running-right.png", 32)
        self.running_left = helper.load_sprites("assets/sprites/player-running-left.png", 32)
        self.idle_right = helper.load_sprites("assets/sprites/idle-right.png", 32)
        self.idle_left = helper.load_sprites("assets/sprites/idle-left.png", 32)



    def apply(self, player):
        player.speed = self.base_speed
        player.color = self.color
        player.jump_force = self.base_jump_force
        player.health = self.base_health
        player.defense = self.base_defense
        player.attack = self.base_attack
        player.can_fly = False

        player.animations = {
            "idle_right": self.idle_right,
            "idle_left": self.idle_left,
            "run_right": self.running_right,
            "run_left": self.running_left
        }

        player.state = "idle"
        player.facing = "right"
        player.current_animation_state = "idle_right"

        # Save bottom center (this is enough)
        bottom_center = player.rect.midbottom

        # Resize
        player.rect.width = 18
        player.rect.height = 20

        # Restore alignment
        player.rect.midbottom = bottom_center

        # Sync position
        player.position.x = player.rect.x
        player.position.y = player.rect.y

        # Adjust sprite offset
        player.draw_offset.x = -(32 - player.rect.width) // 2
        player.draw_offset.y = -(32 - player.rect.height) + 4

    def detect_animation(self, player):
        if player.velocity_x > 0:
            player.state = "run"
            player.facing = "right"
        elif player.velocity_x < 0:
            player.state = "run"
            player.facing = "left"
        else:
            player.state = "idle"


