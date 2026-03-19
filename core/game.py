import pygame
from config import *
from utils.constants import *
from .input_handler import InputHandler
from entities.player import Player
from entities.enemy import Enemy
from world.tilemap import TileMap

class Game:

    # Initializes the game objects
    def __init__(self):
        self.player_position = pygame.Vector2()
        self.enemy_position = pygame.Vector2()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.InputHandler = InputHandler()
        self.TileMap = TileMap()
        self.tile_rects = self.TileMap.get_tile_rects()
        self.player_position.x = 200
        self.player_position.y = 600

        self.enemy_position.x = 700
        self.enemy_position.y = 200

        self.player = Player(self.player_position, BASE_VELOCITY, self.tile_rects)
        self.player_rect = self.player.get_player_rect()
        self.enemy = Enemy(self.enemy_position, BASE_VELOCITY * 0.5, self.tile_rects, self.player)

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
        self.enemy.update(dt)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.TileMap.draw(self.screen)
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        pygame.display.flip()