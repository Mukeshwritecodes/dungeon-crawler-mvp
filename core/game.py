import pygame
from config import *
from systems.combat_system import CombatSystem
from systems.xp_system import XPSystem
from utils.constants import *
from .input_handler import InputHandler
from entities.player import Player
from entities.enemy import Enemy
from world.tilemap import TileMap
from world.camera import Camera

class Game:

    # Initializes the game objects
    def __init__(self):

        # Important game object initialization
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.world_surface = pygame.Surface((WIDTH, HEIGHT))  # base resolution
        self.zoom = ZOOM
        self.camera_speed = CAMERA_SPEED
        self.clock = pygame.time.Clock()
        self.InputHandler = InputHandler()
        self.TileMap = TileMap()
        self.tile_rects = self.TileMap.get_tile_rects()

        # Player and Enemy objects
        self.player_position = pygame.Vector2()
        self.enemy1_position = pygame.Vector2()
        self.enemy2_position = pygame.Vector2()

        self.player_position.x = 447
        self.player_position.y = 3300
        self.player = Player(self.player_position, self.tile_rects)
        self.player_rect = self.player.get_player_rect()

        self.camera = pygame.math.Vector2(
            self.player_rect.centerx - WIDTH // 2,
            self.player_rect.centery - HEIGHT // 2
        )
        self.offset = -self.camera

        self.enemy1_position.x = 800
        self.enemy1_position.y = 3303
        self.enemy1 = Enemy(self.enemy1_position, self.tile_rects, self.player)

        self.enemy2_position.x = 600
        self.enemy2_position.y = 3303
        self.enemy2 = Enemy(self.enemy2_position, self.tile_rects, self.player)

        self.enemies = [self.enemy1, self.enemy2]
        self.combat_system = CombatSystem()

        self.running = True

        self.vignette_surface = pygame.image.load("assets/tilesets/backgrounds/Vignette.png").convert_alpha()
        self.vignette_surface = pygame.transform.scale(self.vignette_surface,(WIDTH, HEIGHT))
        self.vignette_surface.set_colorkey((0, 0, 0))  # remove black

        self.xp_system = XPSystem()


    # Runs the main game loop and call the draw and update methods
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

        '''If player wants to attack,
         the combat system is called to compute the damage and handle the death'''
        if self.player.wants_to_attack:
            for enemy in self.enemies:
                self.combat_system.attack(self.player, enemy)

            self.player.wants_to_attack = False

        # Enemy attack works the same as the player attack
        for enemy in self.enemies:
            if enemy.wants_to_attack:
                self.combat_system.attack(enemy, self.player)
                self.player.wants_to_attack = False


        self.player.update(dt, self.InputHandler.movement_handler(events))
        for enemy in self.enemies:
            enemy.update(dt)
            if not enemy.is_alive:
                self.xp_system.calculate_xp(self.player, enemy.type, enemy.xp)

        self.enemies = [e for e in self.enemies if e.is_alive] # Only the alive enemies are stored

        camera_rect = Camera.update_camera(self.player_rect, self.camera, self.camera_speed)
        camera = pygame.math.Vector2(camera_rect.x, camera_rect.y)
        self.offset = -camera


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
        return True

    def draw(self):
        # 1. Draw everything on world surface
        self.world_surface.fill((0, 0, 0))

        self.TileMap.draw(self.world_surface, self.offset)
        self.player.draw(self.world_surface, self.offset)

        for enemy in self.enemies:
            enemy.draw(self.world_surface, self.offset)

        # 2. Scale according to the zoom
        scaled_surface = pygame.transform.scale(
            self.world_surface,
            (int(self.world_surface.get_width() * self.zoom),
             int(self.world_surface.get_height() * self.zoom))
        )

        screen_rect = self.screen.get_rect()
        scaled_rect = scaled_surface.get_rect(center=screen_rect.center)

        self.screen.blit(scaled_surface, scaled_rect)
        self.screen.blit(self.vignette_surface, (0, 0))

        pygame.display.flip()



