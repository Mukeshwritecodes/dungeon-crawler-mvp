import pygame
import math
from entities.enemy import Enemy
from utils.helpers import Helper


class BatMonster(Enemy):
    def __init__(self, position, tile_rects, player):
        super().__init__(position, tile_rects, player)

        helper = Helper()

        # ----- STATS ----- #
        self.speed = 120
        self.health = 200
        self.attack = 300
        self.type = "bat"
        self.xp = 90
        bottom = self.rect.bottom  # preserve ground alignment

        self.rect.width = 32
        self.rect.height = 32

        self.rect.bottom = bottom  # restore alignment

        self.draw_offset = pygame.Vector2(0, 0)

        sprite_width = 22
        sprite_height = 22

        self.draw_offset.x = -(sprite_width - self.rect.width) // 2
        self.draw_offset.y = -(sprite_height - self.rect.height)

        # ----- FLAGS ----- #
        self.affected_by_gravity = False

        # ----- ANIMATION ----- #
        self.flying_right = helper.load_sprites("assets/sprites/bat-flying-right.png", 32)
        self.flying_left = helper.load_sprites("assets/sprites/bat-flying-left.png", 32)

        self.animations = {
            "fly_right": self.flying_right,
            "fly_left": self.flying_left
        }

        self.frame_index = 0
        self.animation_speed = 0.15
        self.animation_timer = 0

        self.state = "fly"
        self.facing = "left"
        self.current_animation_state = "fly_left"
        self.current_animation = self.animations[self.current_animation_state]
        self.following = False
        self.disagro_counter = 0
        self.disagro_timer = 3
        self.attack_cooldown = 0

    # ----- MOVEMENT (FLYING AI) ----- #
    def move(self, dt):

        if self.distance_to_player() < 100:
            self.following = True

        if self.following and self.distance_to_player() > 300:
            self.disagro_counter += dt
            if self.disagro_counter > self.disagro_timer:
                self.disagro_counter = 0
                self.following = False


        if self.following:

            dx = self.player.rect.centerx - self.position.x
            dy = self.player.rect.centery - self.position.y

            distance = math.hypot(dx, dy)

            if distance < 10:
                self.velocity_x = 0
                self.velocity_y = 0
                return

            dx /= distance
            dy /= distance

            self.velocity_x = dx * self.speed
            self.velocity_y = dy * self.speed

        else:
            self.velocity_x = 0
            self.velocity_y = 0

    # ----- UPDATE ----- #
    def update(self, dt):
        super().update(dt)

        self.update_animation(dt)
        self.handle_attack(dt)

    # ----- ANIMATION ----- #
    def update_animation(self, dt):
        if self.velocity_x > 0:
            self.facing = "right"
        elif self.velocity_x < 0:
            self.facing = "left"

        new_state = f"fly_{self.facing}"

        if new_state != self.current_animation_state:
            self.current_animation_state = new_state
            self.current_animation = self.animations[new_state]
            self.frame_index = 0

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_animation)

    # ----- DRAW ----- #
    def draw(self, screen, offset):
        sprite = self.current_animation[self.frame_index]
        draw_pos = (
            self.rect.x + offset[0] + self.draw_offset.x,
            self.rect.y + offset[1] + self.draw_offset.y
        )

        screen.blit(sprite, draw_pos)

    # ----- COMBAT ----- #
    def handle_attack(self, dt):
        self.attack_cooldown -= dt

        if self.rect.colliderect(self.player.rect):
            if self.attack_cooldown <= 0:
                self.wants_to_attack = True
                self.attack_cooldown = 1  # 1 second