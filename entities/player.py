from typing import override

import pygame

from .entity_base import EntityBase
from utils import constants

class Player(EntityBase):
    def __init__(self, name, entity_type, position, velocity):
        super().__init__(name, entity_type, position, velocity)
        self.is_jumping = False
        self.jump_height = -2
        self.ground_y = 400


    def update(self, dt, action):
        self.move(dt, action)
        self.gravity(dt)
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.position.x, self.position.y, 100, 50))

    def move(self, dt, actions):
        for action in actions:
            match action:
                case "LEFT":
                    print("I reached LEFT")
                    self.position.x -= self.velocity * dt
                case "RIGHT":
                    print("I reached RIGHT")
                    self.position.x += self.velocity * dt
                case "JUMP":
                    print("I reached JUMP")
                    if not self.is_jumping:
                        is_jumping = True
                        self.position.y = self.jump_height
                #case "CROUCH":
                 #   self.position.y -= self.velocity.y * dt


    def gravity(self, dt):
        gravity = constants.GRAVITY
        self.velocity += gravity * dt
        self.position.y += self.velocity * dt
        if self.position.y > self.ground_y:
            self.is_jumping = False
            self.jump_height = -self.jump_height
            self.position.y = self.ground_y
