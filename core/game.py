import pygame
from config import *
from systems.combat_system import CombatSystem
from systems.xp_system import XPSystem
from systems.ui_system import UISystem
from systems.sound_manager import SoundManager
from .input_handler import InputHandler
from entities.player import Player
from world.tilemap import TileMap
from world.camera import Camera

from entities.enemyTypes.mobs.slime_monster import SlimeMonster
from entities.enemyTypes.mobs.bat_monster import BatMonster
from entities.enemyTypes.bosses.mud_golem import MudGolem


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
        self.spike_rects = self.TileMap.get_spike_rects()
        self.sound = SoundManager()

        # Player and Enemy objects
        self.player_position = pygame.Vector2()
        self.enemy1_position = pygame.Vector2()
        self.enemy2_position = pygame.Vector2()

        self.player_position.x = 160
        self.player_position.y = 1120
        self.player = Player(self.player_position, self.tile_rects,self.sound)
        self.player_rect = self.player.get_player_rect()

        self.camera = pygame.math.Vector2(0, 0)
        self.offset = -self.camera
        self.respawn_timer = 0
        self.respawn_delay = 1.5

        self.enemies = []

        enemy_types = {
            "slime": SlimeMonster,
             "bat": BatMonster,
            "mud_golem" : MudGolem,
        }

        enemy_data = [
            ("slime", 2048, 1120),
            ("slime", 2000, 1120),
            ("slime", 1950, 1120),
            ("bat", 1536, 320),
            ("bat", 1510, 332),
            ("bat", 1490, 310),
            ("bat", 1560, 300),
            ("mud_golem", 3328, 1152),
        ]

        for etype, x, y in enemy_data:
            cls = enemy_types[etype]
            self.enemies.append(cls(pygame.Vector2(x, y), self.tile_rects, self.player))


        self.running = True

        self.vignette_surface = pygame.image.load("assets/tilesets/backgrounds/Vignette.png").convert_alpha()
        self.vignette_surface = pygame.transform.scale(self.vignette_surface,(WIDTH, HEIGHT))
        self.vignette_surface.set_colorkey((0, 0, 0))  # remove black
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay.set_alpha(100)
        self.overlay.fill((255, 0, 0))

        self.combat_system = CombatSystem(self.sound)
        self.xp_system = XPSystem()
        self.ui = UISystem()
        self.game_state = "menu"




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

        if self.game_state == "menu":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_state = "playing"
            return

        if self.game_state == "paused":
            return

        if self.game_state == "playing":
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
                    enemy.wants_to_attack = False


            self.player.update(dt, self.InputHandler.movement_handler(events))

            if not self.player.is_alive:
                self.respawn_timer += dt

                if self.respawn_timer >= self.respawn_delay:
                    self.respawn_timer = 0
                    self.enemies = []

                    enemy_types = {
                        "slime": SlimeMonster,
                        "bat": BatMonster,
                        "mud_golem": MudGolem,
                    }

                    enemy_data = [
                        ("slime", 2048, 1120),
                        ("slime", 2000, 1120),
                        ("slime", 1950, 1120),
                        ("bat", 1536, 320),
                        ("bat", 1510, 332),
                        ("bat", 1490, 310),
                        ("bat", 1560, 300),
                        ("mud_golem", 3328, 1152),
                    ]

                    for etype, x, y in enemy_data:
                        cls = enemy_types[etype]
                        self.enemies.append(cls(pygame.Vector2(x, y), self.tile_rects, self.player))





            for spike in self.spike_rects:
                if self.player.rect.colliderect(spike):
                    self.player.is_alive = False


            for enemy in self.enemies:
                enemy.update(dt)
                if not enemy.is_alive:
                    self.xp_system.calculate_xp(self.player, enemy.type, enemy.xp)

            self.enemies = [e for e in self.enemies if e.is_alive] # Only the alive enemies are stored

            self.player_rect = self.player.get_player_rect()

            camera_rect = Camera.update_camera(self.player_rect, self.camera, self.camera_speed)
            camera = pygame.Vector2(camera_rect.x, camera_rect.y)
            self.offset = -camera

    def handle_events(self, events):
        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.game_state = "paused"
                    else:
                        self.game_state = "playing"

            if event.type == pygame.QUIT:
                return False

        return True

    def draw(self):

        if self.game_state == "playing":
            # 1. Draw everything on world surface
            self.world_surface.fill((0, 0, 0))

            self.TileMap.draw(self.world_surface, self.offset)
            self.player.draw(self.world_surface, self.offset)

            for enemy in self.enemies:
                enemy.draw(self.world_surface, self.offset)

            # 2. Scale according to the zoom
            scaled_surface = pygame.transform.scale(
                self.world_surface,
                (int(WIDTH * self.zoom), int(HEIGHT * self.zoom))
            )

            scaled_width = scaled_surface.get_width()
            scaled_height = scaled_surface.get_height()

            offset_x = (scaled_width - WIDTH) // 2
            offset_y = (scaled_height - HEIGHT) // 2

            self.screen.blit(scaled_surface, (-offset_x, -offset_y))

            self.screen.blit(self.vignette_surface, (0, 0))
            self.ui.draw_hud(self.screen, self.player)

            if not self.player.is_alive:
                self.screen.blit(self.overlay, (0, 0))


        if self.game_state == "paused":
            self.ui.draw_pause(self.screen)
        if self.game_state == "menu":
            self.ui.draw_menu(self.screen)
            pygame.display.flip()
            return

        pygame.display.flip()



