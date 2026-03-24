from PIL.ImageChops import offset

from forms.base_form import BaseForm
from utils import constants
from utils.helpers import Helper


class BatForm(BaseForm):

    def __init__(self):
        super().__init__()
        helper = Helper()

        self.flying_right = helper.load_sprites("assets/sprites/bat-flying-right.png", 32)
        self.flying_left = helper.load_sprites("assets/sprites/bat-flying-left.png", 32)


    def apply(self, player):

        multiplier = {
            "speed": 1.2,
            "jump_force": 0.3,
            "health": 0.75,
            "defense": 0.75,
            "attack": 1.5
        }

        player.speed = self.base_speed * multiplier["speed"]
        player.jump_force = self.base_jump_force * multiplier["jump_force"]
        player.health = self.base_health * multiplier["health"]
        player.max_health = self.base_max_health * multiplier["health"]
        player.defense = self.base_defense * multiplier["defense"]
        player.attack = self.base_attack * multiplier["attack"]
        player.can_fly = True

        player.animations = {
            "fly_right": self.flying_right,
            "fly_left": self.flying_left
        }

        player.state = "fly"
        player.facing = "right"
        player.current_animation_state = "fly_right"

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
        player.draw_offset.y = -(32 - player.rect.height) + 5


    def detect_animation(self, player):
        if player.velocity_x > 0:
            player.state = "fly"
            player.facing = "right"
        elif player.velocity_x < 0:
            player.state = "fly"
            player.facing = "left"
