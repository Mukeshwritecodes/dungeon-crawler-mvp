import pygame
from config import *
from systems.combat_system import CombatSystem
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
        self.player_position.x = 447
        self.player_position.y = 3303

        self.enemy1_position.x = 447
        self.enemy1_position.y = 3303

        self.player = Player(self.player_position, self.tile_rects)
        self.player_rect = self.player.get_player_rect()
        self.enemy1 = Enemy(self.enemy1_position, BASE_SPEED * 0.3, self.tile_rects, self.player)
        self.enemy2_position.x = 447
        self.enemy2_position.y = 3303
        self.enemy2 = Enemy(self.enemy2_position, BASE_SPEED * 0.5, self.tile_rects, self.player)
        self.camera = pygame.math.Vector2(0, 0)
        self.offset = 0

        self.enemies = [self.enemy1, self.enemy2]
        self.combat_system = CombatSystem()

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

        if self.player.wants_to_attack:
            for enemy in self.enemies:
                self.combat_system.attack(self.player, enemy)

            self.player.wants_to_attack = False

        for enemy in self.enemies:
            if enemy.wants_to_attack:
                self.combat_system.attack(enemy, self.player)
                self.player.wants_to_attack = False


        self.player.update(dt, self.InputHandler.movement_handler(events))
        for enemy in self.enemies:
            enemy.update(dt)
            enemy.update(dt)
            self.enemies = [e for e in self.enemies if e.is_alive]

        camera_rect = Camera.update_camera(self.player_rect, self.camera)
        camera = pygame.math.Vector2(camera_rect.x, camera_rect.y)
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
        for enemy in self.enemies:
            enemy.draw(self.screen, self.offset)
            enemy.draw(self.screen, self.offset)

        pygame.display.flip()

