import pygame

from entities.enemy import Enemy
from utils.helpers import Helper


class MudGolem(Enemy):
    def __init__(self, position, tile_rects, player):
        super().__init__(position, tile_rects, player)

        helper = Helper()

        # ----- STATS ----- #
        self.jump_force = -240
        self.speed = 50
        self.health = 5000
        self.attack = 150
        self.type = "mud_golem"
        self.xp = 800
        # ------------------ #

        bottom = self.rect.bottom  # preserve ground alignment

        self.rect.width = 64
        self.rect.height = 64

        self.rect.bottom = bottom  # restore alignment

        self.draw_offset = pygame.Vector2(0, 0)

        sprite_width = 48
        sprite_height = 50

        self.draw_offset.x = -(sprite_width - self.rect.width) // 2
        self.draw_offset.y = -(sprite_height - self.rect.height)

        # -------Animation--------#
        self.walking_right = helper.load_sprites("assets/sprites/golem-walking-right.png", 64)
        self.walking_left = helper.load_sprites("assets/sprites/golem-walking-left.png", 64)
        self.idle_right = helper.load_sprites("assets/sprites/golem-idle-right.png", 64)
        self.idle_left = helper.load_sprites("assets/sprites/golem-idle-right.png", 64)


        self.animations = {
            "idle_right": self.idle_right,
            "idle_left": self.idle_left,
            "walk_right": self.walking_right,
            "walk_left": self.walking_left,
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


    def update(self, dt):
        super().update(dt)

        self.update_animation(dt)
        self.handle_attack()

    # ----- ANIMATION SYSTEM ----- #
    def update_animation(self, dt):
        # Detect state
        if self.velocity_x != 0:
            self.state = "walk"
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