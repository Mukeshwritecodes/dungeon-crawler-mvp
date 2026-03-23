from forms.base_form import BaseForm
from utils import constants
from utils.helpers import Helper


class SlimeForm(BaseForm):

    def __init__(self):
        BaseForm.__init__(self)
        helper = Helper()

        self.running_right = helper.load_sprites("assets/sprites/slime-walking-right.png", 16)
        self.running_left = helper.load_sprites("assets/sprites/slime-walking-left.png", 16)
        self.idle_right = helper.load_sprites("assets/sprites/slime-idle-right.png", 16)
        self.idle_left = helper.load_sprites("assets/sprites/slime-idle-left.png", 16)
        self.jumping_right = helper.load_sprites("assets/sprites/slime-jump-right.png", 16)
        self.jumping_left = helper.load_sprites("assets/sprites/slime-jump-left.png", 16)

        self.state = "idle"
        self.facing = "right"
        self.current_animation_state = "idle_right"

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

        player.animations = {
            "idle_right": self.idle_right,
            "idle_left": self.idle_left,
            "run_right": self.running_right,
            "run_left": self.running_left,
            "jump_right": self.jumping_right,
            "jump_left": self.jumping_left,
        }

        player.rect.height = 16
        player.rect.width = 16

    def detect_animation(self, player):
        if player.velocity_y < 0:
            if player.velocity_x > 0:
                player.state = "jump"
                player.facing = "right"
            else:
                player.state = "jump"
                player.facing = "left"
        elif player.velocity_x > 0:
            player.state = "run"
            player.facing = "right"
        elif player.velocity_x < 0:
            player.state = "run"
            player.facing = "left"

        else:
            player.state = "idle"
