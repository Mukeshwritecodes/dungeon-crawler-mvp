import pygame
from config import *
#import input_handler

class Game:

    # Initializes the game objects
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    # Runs the main game loop and call the important functions
    def run(self):

        running = True

        # Loop until 'X' is pressed
        while running:
            dt = self.clock.tick(FPS) / 1000
            running = self.handle_events()
            self.update(dt)
            self.draw()

    def update(self, dt):
        # working...
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()