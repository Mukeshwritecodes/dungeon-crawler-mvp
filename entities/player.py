import pygame

from forms.base_form import BaseForm
from utils.constants import BASE_SPEED, BASE_JUMP_FORCE
from .entity_base import EntityBase
from utils import constants
from utils.helpers import Helper
from systems.transformation_system import TransformationSystem


class Player(EntityBase):
    def __init__(self, position, tile_rects):
        super().__init__(position, BASE_SPEED)

        self.rect = pygame.Rect(self.position.x, self.position.y, 25, 25)
        self.tile_rects = tile_rects
        self.rectangle_surface = pygame.Surface((25, 25))

        self.wants_to_attack = False
        self.is_jumping = False
        self.is_flying = False
        self.is_alive = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 0
        self.color = 0
        self.jump_force = 0
        self.health = 10000
        self.defense = 0
        self.attack = 100
        self.fortitude = 0
        self.form = BaseForm().apply(self)
        self.transformation_system = TransformationSystem()

        helper = Helper()
        self.running_right = helper.load_sprites("assets/sprites/player-running-right.png", 32)
        self.running_left = helper.load_sprites("assets/sprites/player-running-left.png", 32)
        self.idle_right = helper.load_sprites("assets/sprites/idle-right.png", 32)
        self.idle_left = helper.load_sprites("assets/sprites/idle-left.png", 32)
        self.animations = {
            "idle_right": self.idle_right,
            "idle_left": self.idle_left,
            "run_right": self.running_right,
            "run_left": self.running_left
        }
        self.spritesheet_index = 0
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1

        self.state = "idle"
        self.facing = "right"
        self.current_animation = "idle_right"

    def update(self, dt, actions):
        # Reset horizontal velocity each frame so player stops when key is released
        self.velocity_x = 0
        if self.is_flying:
            self.velocity_y = 0

        # 1. Handle Input & Horizontal Movement
        self.handle_input(actions)
        self.position.x += self.velocity_x * dt
        self.rect.x = self.position.x  # Sync rect for collision check
        self.check_collision_x()

        # 2. Handle Gravity & Vertical Movement
        self.apply_gravity(dt)
        self.position.y += self.velocity_y * dt
        self.rect.y = self.position.y  # Sync rect for collision check
        self.check_collision_y()

        if self.velocity_x > 0:
            self.state = "run"
            self.facing = "right"
        elif self.velocity_x < 0:
            self.state = "run"
            self.facing = "left"
        else:
            self.state = "idle"

        self.current_animation = self.animations[f"{self.state}_{self.facing}"]

        self.animation_timer += dt

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index += 1

            if self.frame_index >= len(self.current_animation):
                self.frame_index = 0


    def draw(self, screen, offset):

        #self.rectangle_surface.fill(self.color)
        #draw_pos = (self.rect.x + offset[0], self.rect.y + offset[1])
        #screen.blit(self.rectangle_surface, draw_pos)

        sprite = self.current_animation[self.frame_index]
        screen.blit(sprite, self.rect.move(offset))
        new_state = f"{self.state}_{self.facing}"

        if new_state != self.current_animation:
            self.current_animation = new_state
            self.frame_index = 0


    def handle_input(self, actions):
        for action in actions:
            match action:
                case "RIGHT":
                    self.velocity_x = self.speed
                    self.spritesheet_index = 0
                    self.frame_index = 0
                case "LEFT":
                    self.velocity_x = -self.speed
                    self.spritesheet_index = 1
                    self.frame_index = 1
                case "JUMP":
                    if self.is_flying:
                        self.velocity_y = self.jump_force
                    if not self.is_jumping and not self.is_flying:
                        self.velocity_y = self.jump_force
                        self.is_jumping = True
                case "DOWN":
                    if self.is_flying:
                        self.velocity_y = -self.jump_force
                case "TRANSFORM":
                    self.transformation_system.transform(self)

                case "ATTACK":
                    self.wants_to_attack = True


    def apply_gravity(self, dt):
        # Apply constant gravity force
        if not self.is_flying:
            self.velocity_y += constants.GRAVITY * dt
            if self.velocity_y > constants.TERMINAL_VELOCITY:
                self.velocity_y = constants.TERMINAL_VELOCITY

    def check_collision_x(self):
        # Check tiles specifically for horizontal overlaps
        rect = self.get_collision_rect(self.rect)
        if rect:
            if self.velocity_x > 0:  # Moving Right
                self.position.x = rect.left - self.rect.width
            elif self.velocity_x < 0:  # Moving Left
                self.position.x = rect.right
            self.rect.x = self.position.x  # Snap rect to new position

    def check_collision_y(self):
        # Check tiles specifically for vertical overlaps (Floor/Ceiling)
        rect = self.get_collision_rect(self.rect)
        if rect:
            if self.velocity_y > 0:  # Falling (Hitting floor)
                self.position.y = rect.top - self.rect.height
                self.velocity_y = 0
                self.is_jumping = False  # Reset jump ability
            elif self.velocity_y < 0:  # Jumping (Hitting ceiling)
                self.position.y = rect.bottom
                self.velocity_y = 0
            self.rect.y = self.position.y  # Snap rect to new position

    def get_collision_rect(self, obj_rect):
        # Returns the tile rect we collided with, or None
        for rect in self.tile_rects:
            if obj_rect.colliderect(rect):
                return rect
        return None

    def get_player_rect(self):
        return self.rect


