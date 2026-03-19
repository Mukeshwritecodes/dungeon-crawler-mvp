import pygame
from config import *
from utils.constants import *
from .input_handler import InputHandler
from entities.player import Player
from world.tilemap import TileMap

class Game:

    # Initializes the game objects
    def __init__(self):
        self.position = pygame.Vector2()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.InputHandler = InputHandler()
        self.TileMap = TileMap()
        self.tile_rects = self.TileMap.get_tile_rects()
        print(self.tile_rects)
        self.position.x = 200
        self.position.y = 400

        self.player = Player("player", 1, self.position, BASE_VELOCITY, self.tile_rects)


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
        self.player.update(dt, self.InputHandler.movement_handler())

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.TileMap.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()