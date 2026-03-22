import pygame
import math
from entities.entity_base import EntityBase
from utils import constants
from utils.helpers import Helper


class Enemy(EntityBase):
    def __init__(self, position, tile_rects, player):
        super().__init__(position)

        helper = Helper()
        self.jump_force = -200  # Increased for dt scaling
        self.tile_rects = tile_rects
        self.is_alive = True
        self.is_jumping = False
        self.wants_to_attack = False
        self.speed = constants.BASE_SPEED * 0.5
        self.health = 500
        self.defense = 250
        self.attack = 50


        self.velocity_x = 0
        self.velocity_y = 0
        self.player_rect = player.get_player_rect()
        self.rect = pygame.Rect(self.position.x, self.position.y, 16, 16)

        # -------Animation loading--------#
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

        self.spritesheet_index = 0
        self.frame_index = 0
        self.animation_speed = 0.1  # Time between each frame
        self.animation_timer = 0  # Clock to make sure speed is constant at 0.1

        self.state = "idle"
        self.facing = "left"
        self.current_animation_state = "idle_left"
        self.current_animation = []
        # ---------------------------------#

    def update(self, dt):

        # If the player is above and the enemy is not already jumping, it will jump
        if not self.is_jumping and self.player_y_direction() == -1:
            self.velocity_y = self.jump_force
            self.is_jumping = True
            if self.player_x_direction() == -1:
                self.spritesheet_index = 4 # Right jump
            else:
                self.spritesheet_index = 5 # Left jump
        # Not jumping
        else:
            if self.player_y_direction() == -1:
                self.spritesheet_index = 2 # Running right
            else:
                self.spritesheet_index = 3 # Running left


        '''If the enemy and the player rect collides, then
         the player is in the enemy's range, and it can attack'''
        if self.rect.colliderect(self.player_rect):
            self.wants_to_attack = True

        self.velocity_x = 0
        # 1. Horizontal movement
        self.velocity_x = self.player_x_direction() * self.speed
        self.position.x += self.velocity_x * dt
        self.rect.x = self.position.x
        self.check_collision_x()

        # 2. Handle Gravity & vertical movement
        self.apply_gravity(dt)
        self.position.y += self.velocity_y * dt
        self.rect.y = self.position.y
        self.check_collision_y()

        #-----Animation detection-----#
        if self.velocity_y < 0:
            if self.velocity_x > 0:
                self.state = "jump"
                self.facing = "right"
            else:
                self.state = "jump"
                self.facing = "left"
        elif self.velocity_x > 0:
            self.state = "run"
            self.facing = "right"
        elif self.velocity_x < 0:
            self.state = "run"
            self.facing = "left"

        else:
            self.state = "idle"

        self.current_animation = self.animations[f"{self.state}_{self.facing}"]
        # Clock
        self.animation_timer += dt

        # Increment frame index and reset the clock
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index += 1

            # Reset frame index to avoid index out of bound and continue the animation loop
            if self.frame_index >= len(self.current_animation):
                self.frame_index = 0

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
        screen.blit(sprite, self.rect.move(offset))


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


    '''Checks horizontal collision. If there's collision, then
     depending on the direction of the enemy's movement, it is snapped 
     to the edge of the tile'''
    def check_collision_x(self):
        rect = self.get_collision_rect(self.rect)
        if rect:
            if self.velocity_x > 0:  # Moving Right
                self.position.x = rect.left - self.rect.width
            elif self.velocity_x < 0:  # Moving Left
                self.position.x = rect.right
            self.rect.x = self.position.x  # Snap rect to new position

    # Same as horizontal collision check.
    def check_collision_y(self):
        # Check tiles specifically for vertical overlaps (Floor/Ceiling)
        rect = self.get_collision_rect(self.rect)
        if rect:
            if  self.velocity_y > 0:  # Falling (Hitting floor)
                self.position.y = rect.top - self.rect.height
                self.velocity_y = 0
                self.is_jumping = False # Resetting jump
            elif self.velocity_y < 0:  # Jumping (Hitting ceiling)
                self.position.y = rect.bottom
                self.velocity_y = 0
            self.rect.y = self.position.y  # Snap rect to new position

    # identifies players horizontal direction to follow
    def player_x_direction(self):
        distance = self.player_rect.x - self.position.x

        if abs(distance) < self.player_rect.width and self.player_rect.x < self.position.x:
            return 0
        elif abs(distance)  < self.rect.width and self.player_rect.x > self.position.x:
            return 0
        return 1 if distance > 0 else -1

    # identifies players vertical direction to toggle jumping
    def player_y_direction(self):
        distance = self.player_rect.y - self.position.y

        if distance + self.player_rect.height > 0:
            return 1 # Player is below
        return -1 # Player is above

    # Calculates the distance between the player and enemy, not used yet
    def calculate_distance(self):
        return math.hypot(self.player_rect.x - self.position.x, self.player_rect.y - self.position.y)