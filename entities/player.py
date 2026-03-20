import pygame

from forms.base_form import BaseForm
from utils.constants import BASE_SPEED
from .entity_base import EntityBase
from utils import constants
from systems.transformation_system import TransformationSystem


class Player(EntityBase):
    def __init__(self, position, tile_rects):
        super().__init__(position, BASE_SPEED)

        self.tile_rects = tile_rects
        self.is_jumping = False
        self.jump_force = -900  # Increased for dt scaling
        self.velocity_x = 0
        self.velocity_y = 0
        self.player_rect = pygame.Rect(self.position.x, self.position.y, 50, 100)
        self.speed = BASE_SPEED
        self.color = constants.BLUE
        self.form = BaseForm()
        self.transformation_system = TransformationSystem()

    def update(self, dt, actions):
        # Reset horizontal velocity each frame so player stops when key is released
        self.velocity_x = 0

        # 1. Handle Input & Horizontal Movement
        self.handle_input(actions)
        self.position.x += self.velocity_x * dt
        self.player_rect.x = self.position.x  # Sync rect for collision check
        self.check_collision_x()

        # 2. Handle Gravity & Vertical Movement
        self.apply_gravity(dt)
        self.position.y += self.velocity_y * dt
        self.player_rect.y = self.position.y  # Sync rect for collision check
        self.check_collision_y()

    def draw(self, screen, offset):
        # Drawing the player as a blue rectangle
        # Create the surface (do this once, not every frame, for better performance)
        rectangle_surface = pygame.Surface((50, 100))
        rectangle_surface.fill(self.color)

        # Calculate the draw position by adding the offset to the player's rect
        draw_pos = (self.player_rect.x + offset[0], self.player_rect.y + offset[1])

        screen.blit(rectangle_surface, draw_pos)

    def handle_input(self, actions):
        for action in actions:
            match action:
                case "LEFT":
                    self.velocity_x = -self.speed
                case "RIGHT":
                    self.velocity_x = self.speed
                case "JUMP":
                    if not self.is_jumping:
                        self.velocity_y = self.jump_force
                        self.is_jumping = True
                case "TRANSFORM":
                    self.transformation_system.transform(self)

    def check_collision_x(self):
        # Check tiles specifically for horizontal overlaps
        rect = self.get_collision_rect(self.player_rect)
        if rect:
            if self.velocity_x > 0:  # Moving Right
                self.position.x = rect.left - self.player_rect.width
            elif self.velocity_x < 0:  # Moving Left
                self.position.x = rect.right
            self.player_rect.x = self.position.x  # Snap rect to new position

    def apply_gravity(self, dt):
        # Apply constant gravity force
        self.velocity_y += constants.GRAVITY * dt
        if self.velocity_y > constants.TERMINAL_VELOCITY:
            self.velocity_y = constants.TERMINAL_VELOCITY

    def check_collision_y(self):
        # Check tiles specifically for vertical overlaps (Floor/Ceiling)
        rect = self.get_collision_rect(self.player_rect)
        if rect:
            if self.velocity_y > 0:  # Falling (Hitting floor)
                self.position.y = rect.top - self.player_rect.height
                self.velocity_y = 0
                self.is_jumping = False  # Reset jump ability
            elif self.velocity_y < 0:  # Jumping (Hitting ceiling)
                self.position.y = rect.bottom
                self.velocity_y = 0
            self.player_rect.y = self.position.y  # Snap rect to new position

    def get_collision_rect(self, obj_rect):
        # Returns the tile rect we collided with, or None
        for rect in self.tile_rects:
            if obj_rect.colliderect(rect):
                return rect
        return None

    def get_player_rect(self):
        return self.player_rect