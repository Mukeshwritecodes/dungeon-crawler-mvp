import pygame
import math
from entities.entity_base import EntityBase
from utils import constants


class Enemy(EntityBase):
    def __init__(self, position, tile_rects, player):
        super().__init__(position)

        # ----- Common enemy fields ----- #
        self.is_alive = True
        self.is_jumping = False

        self.velocity_x = 0
        self.velocity_y = 0

        self.jump_force = 0
        self.speed = 0

        self.health = 1
        self.defense = 0
        self.attack = 0
        self.attack_speed = 0

        self.type = "base"
        self.level = 1
        self.xp = 0

        self.wants_to_attack = False

        # Physics flags
        self.affected_by_gravity = True
        self.has_collision = True

        # Rect (hitbox)
        self.rect = pygame.Rect(position.x, position.y, 16, 16)

        # References
        self.player = player
        self.tile_rects = tile_rects
        # -------------------------------- #

    # ----- MAIN UPDATE LOOP ----- #
    def update(self, dt):

        if not self.player.is_alive:
            return

        self.move(dt)  # child defines behavior

        # Horizontal movement
        self.position.x += self.velocity_x * dt
        self.rect.x = self.position.x
        self.check_collision_x()

        # Gravity
        self.apply_gravity(dt)

        # Vertical movement
        self.position.y += self.velocity_y * dt
        self.rect.y = self.position.y
        self.check_collision_y()

    # ----- TO BE OVERRIDDEN BY CHILD ----- #
    def move(self, dt):
        pass

    def draw(self, screen, offset):
        # Simple debug rectangle (you can override in child)
        pygame.draw.rect(screen, (255, 0, 0), self.rect.move(offset), 2)

    # ----- PHYSICS ----- #
    def apply_gravity(self, dt):
        if not self.affected_by_gravity:
            return

        self.velocity_y += constants.GRAVITY * dt

        if self.velocity_y > constants.TERMINAL_VELOCITY:
            self.velocity_y = constants.TERMINAL_VELOCITY

    # ----- COLLISION ----- #
    def get_collision_rect(self):
        for rect in self.tile_rects:
            if self.rect.colliderect(rect):
                return rect
        return None

    def check_collision_x(self):
        if not self.has_collision:
            return

        tile = self.get_collision_rect()
        if tile:
            if self.velocity_x > 0:
                self.rect.right = tile.left
            elif self.velocity_x < 0:
                self.rect.left = tile.right

            self.position.x = self.rect.x

    def check_collision_y(self):
        if not self.has_collision:
            return

        tile = self.get_collision_rect()
        if tile:
            if self.velocity_y > 0:  # Falling
                self.rect.bottom = tile.top
                self.velocity_y = 0
                self.is_jumping = False

            elif self.velocity_y < 0:  # Jumping
                self.rect.top = tile.bottom
                self.velocity_y = 0

            self.position.y = self.rect.y

    # ----- PLAYER RELATION ----- #
    def player_x_direction(self):
        distance = self.player.rect.x - self.position.x
        return 1 if distance > 0 else -1

    def player_y_direction(self):
        distance = self.player.rect.y - self.position.y
        return 1 if distance > 0 else -1

    def distance_to_player(self):
        return math.hypot(
            self.player.rect.x - self.position.x,
            self.player.rect.y - self.position.y
        )

    # ----- COMBAT ----- #
    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.health -= actual_damage

        if self.health <= 0:
            self.is_alive = False