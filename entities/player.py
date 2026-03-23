import pygame

from forms.base_form import BaseForm
from utils.constants import BASE_SPEED, BASE_JUMP_FORCE
from .entity_base import EntityBase
from utils import constants
from utils.helpers import Helper
from systems.transformation_system import TransformationSystem


class Player(EntityBase):
    def __init__(self, position, tile_rects):
        super().__init__(position)

        helper = Helper()
        self.rectangle_surface = pygame.Surface((32, 32))

        # For collision detection and movement
        self.tile_rects = tile_rects
        self.rect = pygame.Rect(self.position.x, self.position.y, 32, 32)

        self.draw_offset = pygame.Vector2(0, 0)

        # Not moving, hence 0
        self.velocity_x = 0
        self.velocity_y = 0

        #------Player status fields------#
        self.is_alive = True
        self.wants_to_attack = False
        self.is_jumping = False
        self.can_fly = False
        self.speed = 0
        self.jump_force = 0
        self.health = 0
        self.defense = 0
        self.attack = 0
        self.fortitude = 0
        self.animations = {}
        self.state = "none"
        self.facing = "none"
        self.current_animation_state = "none"

        self.form = BaseForm()
        self.form.apply(self)
        # Base form initializes all the base stats & animation
        #---------------------------------#

        # Transformation available - Player(Base form), Bat, Slime
        self.transformation_system = TransformationSystem()

        self.frame_index = 0
        self.animation_speed = 0.1 # Time between each frame
        self.animation_timer = 0 # Clock to make sure speed is constant at 0.1

        self.current_animation = []
        # ---------------------------------#

    def update(self, dt, actions):
        # Reset horizontal velocity each frame so player stops when key is released
        self.velocity_x = 0

        # Reset velocity per frame to stop from continues flying or sinking
        if self.can_fly:
            self.velocity_y = 0

        # 1. Handle Input & Horizontal Movement
        self.handle_input(actions)
        self.position.x += self.velocity_x * dt
        self.rect.x = self.position.x # Sync rect for collision check
        self.check_collision_x()

        # 2. Handle Gravity & Vertical Movement
        self.apply_gravity(dt)
        self.position.y += self.velocity_y * dt
        self.rect.y = self.position.y # Sync rect for collision check
        self.check_collision_y()

        #-----Animation detection-----#

        self.form.detect_animation(self)

        # Select the current animation from the dictionary
        self.current_animation = self.animations[f"{self.state}_{self.facing}"]

        # Clock
        self.animation_timer += dt

        # Increment frame index and reset the clock
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            self.frame_index = (self.frame_index + 1) % len(self.current_animation)

        # Select the new state depending upon the input
        new_state = f"{self.state}_{self.facing}"

        # If state isn't the same as before, update state
        if new_state != self.current_animation_state:
            self.current_animation_state = new_state
            self.current_animation = self.animations[new_state]
            self.frame_index = 0


    def draw(self, screen, offset):

        # Select the sprite and render it
        sprite = self.current_animation[self.frame_index]

        draw_x = self.rect.x - (sprite.get_width() - self.rect.width) // 2
        draw_y = self.rect.y - (sprite.get_height() - self.rect.height)

        draw_pos = (
            self.rect.x + offset[0] + self.draw_offset.x,
            self.rect.y + offset[1] + self.draw_offset.y
        )

        screen.blit(sprite, draw_pos)

        #DEBUG - Visible collision rect
        #pygame.draw.rect(screen, (255, 0, 0), self.rect.move(offset), 2)


    def handle_input(self, actions):
        for action in actions:
            match action:

                case "RIGHT":
                    self.velocity_x = self.speed # Positive direction while moving right

                case "LEFT":
                    self.velocity_x = -self.speed # Negative direction while moving right

                case "JUMP":
                    if self.can_fly:
                        self.velocity_y = self.jump_force
                    if not self.is_jumping and not self.can_fly:
                        self.velocity_y = self.jump_force
                        self.is_jumping = True

                case "DOWN":
                    if self.can_fly:
                        self.velocity_y = -self.jump_force

                case "TRANSFORM":
                    self.transformation_system.transform(self)
                    self.velocity_y = 0
                    self.frame_index = 0

                case "ATTACK":
                    self.wants_to_attack = True


    def apply_gravity(self, dt):
        # Apply constant gravity force when not flying
        if not self.can_fly:
            self.velocity_y += constants.GRAVITY * dt
            if self.velocity_y > constants.TERMINAL_VELOCITY:
                self.velocity_y = constants.TERMINAL_VELOCITY

    def check_collision_x(self):
        # Check tiles for horizontal overlaps
        rect = self.get_collision_rect(self.rect)
        if rect:
            if self.velocity_x > 0:  # Moving Right
                self.position.x = rect.left - self.rect.width
            elif self.velocity_x < 0:  # Moving Left
                self.position.x = rect.right
            self.rect.x = self.position.x  # Snap rect to new position

    def check_collision_y(self):
        # Check tiles for vertical overlaps (Floor/Ceiling)
        rect = self.get_collision_rect(self.rect)
        if rect:
            if self.velocity_y > 0:  # Falling (Hitting floor)
                self.rect.bottom = rect.top
                self.position.y = self.rect.y
                self.velocity_y = 0
                self.is_jumping = False  # Reset jump ability
            elif self.velocity_y < 0:  # Jumping (Hitting ceiling)
                self.position.y = rect.bottom
                self.velocity_y = 0
            self.rect.y = self.position.y # Snap rect to new position

    def get_collision_rect(self, obj_rect):
        # Returns the tile rect we collided with, or None
        for rect in self.tile_rects:
            if obj_rect.colliderect(rect):
                return rect
        return None

    def get_player_rect(self):
        return self.rect


