import pygame
from config import WIDTH, HEIGHT
from utils.constants import TILE_SIZE
from utils.helpers import Helper
import csv

class TileMap:

    def __init__(self):
        self.helper = Helper()
        self.path = ["assets/tilesets/backgrounds/BACKGROUND.png",
                "assets/tilesets/backgrounds/WOODS - Fourth.png",
                "assets/tilesets/backgrounds/WOODS - Third.png",
                "assets/tilesets/backgrounds/WOODS - Second.png",
                "assets/tilesets/backgrounds/BUSH - BACKGROUND.png",
                "assets/tilesets/backgrounds/WOODS - First.png",
                "assets/tilesets/backgrounds/VINES - Second.png"]

        self.map_path = "assets/maps/demo_map2.csv"
        self.tileset_path = "assets/tilesets/Tilesheet - WOODS.png"
        self.tile_rects = []

    def update(self):
        pass

    def draw(self, screen, offset):
        self.background(screen)
        self.platform(screen, offset)
        self.foreground()


    def background(self, screen):
        for i in self.path:
            background_surface = self.load_background(i)
            screen.blit(background_surface, (0, 0))

    def platform(self, screen, offset):
        platform_map = self.load_map(self.map_path)
        tileset = self.helper.load_image(self.tileset_path)

        tileset_rows = tileset.height / TILE_SIZE
        tileset_cols = tileset.width / TILE_SIZE

        for row_index, row in enumerate(platform_map):
            for col_index, tile_id in enumerate(row):
                if int(tile_id) != -1:
                    tile_id = int(tile_id)

                    x = int(tile_id % tileset_cols)
                    y = int(tile_id // tileset_cols)

                    tile = self.get_tile(tileset, x * TILE_SIZE, y * TILE_SIZE)
                    tile_rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    screen.blit(tile, tile_rect.move(offset))

    def foreground(self):
        pass


    def get_tile(self, tileset, x, y):
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        return tileset.subsurface(rect)

    def load_background(self, path):
        background_image = self.helper.load_image(path)
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        return background_image


    def load_map(self, path):
        with open(path, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            return list(reader)


    def get_tile_rects(self):
        platform_map = self.load_map(self.map_path)
        for row_index, row in enumerate(platform_map):
            for col_index, tile_id in enumerate(row):
                if int(tile_id) != -1:
                    tile_rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.tile_rects.append(tile_rect)

        return self.tile_rects