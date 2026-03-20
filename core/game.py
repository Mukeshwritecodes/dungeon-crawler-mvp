import pygame
from config import *
from utils.constants import *
from .input_handler import InputHandler
from entities.player import Player
from entities.enemy import Enemy
from world.tilemap import TileMap
from world.camera import Camera

class Game:

    # Initializes the game objects
    def __init__(self):
        self.player_position = pygame.Vector2()
        self.enemy1_position = pygame.Vector2()
        self.enemy2_position = pygame.Vector2()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.InputHandler = InputHandler()
        self.TileMap = TileMap()
        self.tile_rects = self.TileMap.get_tile_rects()
        self.player_position.x = 200
        self.player_position.y = 600

        self.enemy1_position.x = 700
        self.enemy1_position.y = 200

        self.player = Player(self.player_position, self.tile_rects)
        self.player_rect = self.player.get_player_rect()
        self.enemy1 = Enemy(self.enemy1_position, BASE_SPEED * 0.5, self.tile_rects, self.player)
        self.enemy2_position.x = 200
        self.enemy2_position.y = 200
        self.enemy2 = Enemy(self.enemy2_position, BASE_SPEED * 0.5, self.tile_rects, self.player)
        self.camera = pygame.math.Vector2(0, 0)
        self.offset = 0

        self.running = True

    # Runs the main game loop and call the important functions
    def run(self):



        # Loop until 'X' is pressed
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            if dt > 0.05:
                dt = 0.05
            self.update(dt)
            self.draw()

    def update(self, dt):
        events = pygame.event.get()
        self.running = self.handle_events(events)
        self.player.update(dt, self.InputHandler.movement_handler(events))
        self.enemy1.update(dt)
        self.enemy2.update(dt)
        camera = Camera.update_camera(self.player_rect, self.camera)
        self.offset = -camera

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
        return True

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.TileMap.draw(self.screen, self.offset)
        self.player.draw(self.screen, self.offset)
        self.enemy1.draw(self.screen, self.offset)
        self.enemy2.draw(self.screen, self.offset)

        pygame.display.flip()