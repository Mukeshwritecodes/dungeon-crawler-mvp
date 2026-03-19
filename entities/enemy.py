import pygame
import math
from entities.entity_base import EntityBase
from utils import constants


class Enemy(EntityBase):
    def __init__(self, position, speed, tile_rects, player):
        super().__init__(position, speed)

        #self.jump_force = -900  # Increased for dt scaling
        self.tile_rects = tile_rects
        self.is_jumping = False
        self.speed = speed
        self.velocity_x = 0
        self.velocity_y = 0

        self.player_rect = player.get_player_rect()
        self.enemy_rect = pygame.Rect(self.position.x, self.position.y, 25, 25)

    def update(self, dt):
        self.velocity_x = 0
        self.velocity_x = self.player_direction() * self.speed
        self.position.x += self.velocity_x * dt
        self.enemy_rect.x = self.position.x
        self.check_collision_x()

        # 2. Handle Gravity & Vertical Movement
        self.apply_gravity(dt)
        self.position.y += self.velocity_y * dt
        self.enemy_rect.y = self.position.y  # Sync rect for collision check
        self.check_collision_y()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.enemy_rect)

    def apply_gravity(self, dt):
        # Apply constant gravity force
        self.velocity_y += constants.GRAVITY * dt
        if self.velocity_y > constants.TERMINAL_VELOCITY:
            self.velocity_y = constants.TERMINAL_VELOCITY

    def get_collision_rect(self, obj_rect):
        # Returns the tile rect we collided with, or None
        for rect in self.tile_rects:
            if obj_rect.colliderect(rect):
                return rect
        return None

    def check_collision_x(self):
        rect = self.get_collision_rect(self.enemy_rect)
        if rect:
            if self.velocity_x > 0:  # Moving Right
                self.position.x = rect.left - self.enemy_rect.width
            elif self.velocity_x < 0:  # Moving Left
                self.position.x = rect.right
            self.enemy_rect.x = self.position.x  # Snap rect to new position


    def check_collision_y(self):
        # Check tiles specifically for vertical overlaps (Floor/Ceiling)
        rect = self.get_collision_rect(self.enemy_rect)
        if rect:
            if  self.velocity_y > 0:  # Falling (Hitting floor)
                self.position.y = rect.top - self.enemy_rect.height
                self.velocity_y = 0
            elif self.velocity_y < 0:  # Jumping (Hitting ceiling)
                self.position.y = rect.bottom
                self.velocity_y = 0
            self.enemy_rect.y = self.position.y  # Snap rect to new position


    def player_direction(self):
        distance = self.player_rect.x - self.position.x

        if abs(distance) < self.player_rect.width and self.player_rect.x < self.position.x:
            return 0
        elif abs(distance)  < self.enemy_rect.width and self.player_rect.x > self.position.x:
            return 0
        return 1 if distance > 0 else -1


    def calculate_distance(self):
        return math.hypot(self.player_rect.x - self.position.x, self.player_rect.y - self.position.y)