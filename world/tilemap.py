import pygame
from config import WIDTH, HEIGHT
from utils.constants import TILE_SIZE
from utils.helpers import Helper
import csv

class TileMap:

    def __init__(self):

        # Paths for background, map, and tileset
        self.bg_path = ["assets/tilesets/backgrounds/BACKGROUND.png",
                "assets/tilesets/backgrounds/WOODS - Fourth.png",
                "assets/tilesets/backgrounds/WOODS - Third.png",
                "assets/tilesets/backgrounds/WOODS - Second.png",
                "assets/tilesets/backgrounds/BUSH - BACKGROUND.png",
                "assets/tilesets/backgrounds/WOODS - First.png",
                "assets/tilesets/backgrounds/VINES - Second.png"]

        self.map_path = "assets/maps/demo_map2.csv"
        self.tileset_path = "assets/tilesets/Tilesheet - WOODS.png"

        self.helper = Helper()

        # Later for collision
        self.tile_rects = []


    def draw(self, screen, offset):
        self.background(screen)
        self.platform(screen, offset)

    # Draws all the layer of the background in sequence of the path list
    def background(self, screen):
        for i in self.bg_path:
            background_surface = self.load_background(i)
            screen.blit(background_surface, (0, 0))

    # Renders the platforms. Also adds the camera offset
    def platform(self, screen, offset):
        platform_map = self.load_map(self.map_path)
        tileset = self.helper.load_image(self.tileset_path)

        tileset_cols = tileset.width / TILE_SIZE

        # For each column from each row
        for row_index, row in enumerate(platform_map):
            for col_index, tile_id in enumerate(row):

                if int(tile_id) != -1: # -1 if no tile on that place
                    tile_id = int(tile_id) # String to integer

                    x = int(tile_id % tileset_cols) # eg. tile_id(130) % cols(16) = 2nd column
                    y = int(tile_id // tileset_cols) #eg. tile_id(130) // cols(16) = 8th row

                    tile = self.get_tile(tileset, x * TILE_SIZE, y * TILE_SIZE)
                    tile_rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    screen.blit(tile, tile_rect.move(offset))


    # Returns the tile from the tileset
    def get_tile(self, tileset, x, y):
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        return tileset.subsurface(rect)

    # Loads and scales the background image
    def load_background(self, path):
        background_image = self.helper.load_image(path)
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        return background_image

    # Loads the map and returns the list of rows in the map data
    def load_map(self, path):
        with open(path, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            return list(reader)

    # Tile rects for collision
    def get_tile_rects(self):
        platform_map = self.load_map(self.map_path)
        for row_index, row in enumerate(platform_map):
            for col_index, tile_id in enumerate(row):
                if int(tile_id) != -1:
                    tile_rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.tile_rects.append(tile_rect)

        return self.tile_rects