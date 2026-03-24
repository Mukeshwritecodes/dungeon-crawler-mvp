import pygame

from entities.enemy import Enemy
from utils.helpers import Helper


class SlimeMonster(Enemy):
    def __init__(self, position, tile_rects, player):
        super().__init__(position, tile_rects, player)

        helper = Helper()

        # ----- STATS ----- #
        self.jump_force = -240
        self.speed = 60
        self.health = 50
        self.attack = 10
        self.type = "slime"
        self.xp = 80
        # ------------------ #

        bottom = self.rect.bottom  # preserve ground alignment

        self.rect.width = 16
        self.rect.height = 16

        self.rect.bottom = bottom  # restore alignment

        self.draw_offset = pygame.Vector2(0, 0)

        sprite_width = 16
        sprite_height = 16

        self.draw_offset.x = -(sprite_width - self.rect.width) // 2
        self.draw_offset.y = -(sprite_height - self.rect.height)

        # -------Animation--------#
        self.running_right = helper.load_sprites("assets/sprites/slime-walking-right.png", 16)
        self.running_left = helper.load_sprites("assets/sprites/slime-walking-left.png", 16)
        self.idle_right = helper.load_sprites("assets/sprites/slime-idle-right.png", 16)
        self.idle_left = helper.load_sprites("assets/sprites/slime-idle-left.png", 16)
        self.jump_right = helper.load_sprites("assets/sprites/slime-jump-right.png", 16)
        self.jump_left = helper.load_sprites("assets/sprites/slime-jump-left.png", 16)

        self.animations = {
            "idle_right": self.idle_right,
            "idle_left": self.idle_left,
            "run_right": self.running_right,
            "run_left": self.running_left,
            "jump_right": self.jump_right,
            "jump_left": self.jump_left
        }

        self.frame_index = 0
        self.animation_speed = 0.2
        self.animation_timer = 0

        self.state = "idle"
        self.facing = "left"
        self.current_animation_state = "idle_left"
        self.current_animation = self.animations[self.current_animation_state]
        # --------------------------------#

    def move(self, dt):
        self.velocity_x = self.player_x_direction() * self.speed

        # Jump if player is above
        if not self.is_jumping and self.player_y_direction() == -1:
            self.velocity_y = self.jump_force
            self.is_jumping = True

    def update(self, dt):
        super().update(dt)

        self.update_animation(dt)
        self.handle_attack()

    # ----- ANIMATION SYSTEM ----- #
    def update_animation(self, dt):
        # Detect state
        if self.velocity_y < 0:
            self.state = "jump"
        elif self.velocity_x != 0:
            self.state = "run"
        else:
            self.state = "idle"

        if self.velocity_x > 0:
            self.facing = "right"
        elif self.velocity_x < 0:
            self.facing = "left"

        new_state = f"{self.state}_{self.facing}"

        if new_state != self.current_animation_state:
            self.current_animation_state = new_state
            self.current_animation = self.animations[new_state]
            self.frame_index = 0

        # Animate
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_animation)

    def draw(self, screen, offset):

        sprite = self.current_animation[self.frame_index]
        draw_pos = (
            self.rect.x + offset[0] + self.draw_offset.x,
            self.rect.y + offset[1] + self.draw_offset.y
        )

        screen.blit(sprite, draw_pos)

    # ----- COMBAT ----- #
    def handle_attack(self):
        if self.rect.colliderect(self.player.rect):
            self.wants_to_attack = True