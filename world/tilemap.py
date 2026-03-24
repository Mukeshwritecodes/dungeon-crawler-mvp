import pygame
from config import WIDTH, HEIGHT
from utils.constants import TILE_SIZE
from utils.helpers import Helper
import csv


class TileMap:

    def __init__(self):

        self.tileset_path = "assets/tilesets/CastleTiles.png"

        self.map_paths = {
            "background": [
                "assets/maps/dungeon tiless_black.csv",
                "assets/maps/dungeon tiless_background.csv",
                "assets/maps/dungeon tiless_decoration.csv",
                "assets/maps/dungeon tiless_Spike.csv"
            ],
            "main": "assets/maps/dungeon tiless_Tile Layer.csv",
            "spikes": "assets/maps/dungeon tiless_Spike.csv",
        }

        self.helper = Helper()

        # ----- LOAD MAPS ONCE ----- #
        self.maps = {}

        for key, paths in self.map_paths.items():
            if isinstance(paths, list):
                self.maps[key] = [self.load_map(p) for p in paths]
            else:
                self.maps[key] = self.load_map(paths)

        # Load tileset once
        self.tileset = self.helper.load_image(self.tileset_path)

    # ----- DRAW ----- #
    def draw(self, screen, offset):

        # Background layers
        for layer_map in self.maps["background"]:
            self.render_layer(screen, layer_map, offset)

        # Main layer
        self.render_layer(screen, self.maps["main"], offset)

    # ----- RENDER LAYER ----- #
    def render_layer(self, screen, layer_map, offset):

        tileset_cols = self.tileset.get_width() // TILE_SIZE

        for row_index, row in enumerate(layer_map):
            for col_index, tile_id in enumerate(row):

                tile_id = int(tile_id.strip())

                if tile_id != -1:

                    x = tile_id % tileset_cols
                    y = tile_id // tileset_cols

                    tile = self.get_tile(self.tileset, x * TILE_SIZE, y * TILE_SIZE)

                    tile_rect = pygame.Rect(
                        col_index * TILE_SIZE,
                        row_index * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )

                    screen.blit(tile, tile_rect.move(offset))

    # ----- GET TILE ----- #
    def get_tile(self, tileset, x, y):
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        return tileset.subsurface(rect)

    # ----- LOAD MAP ----- #
    def load_map(self, path):
        with open(path, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            return list(reader)

    # ----- COLLISION ----- #
    def get_tile_rects(self):

        tile_rects = []
        main_map = self.maps["main"]

        for row_index, row in enumerate(main_map):
            for col_index, tile_id in enumerate(row):

                tile_id = int(tile_id.strip())

                if tile_id != -1:
                    rect = pygame.Rect(
                        col_index * TILE_SIZE,
                        row_index * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    tile_rects.append(rect)

        return tile_rects

    def get_spike_rects(self):
        spike_rects = []

        spike_map = self.maps["spikes"]

        for row_index, row in enumerate(spike_map):
            for col_index, tile_id in enumerate(row):

                tile_id = int(tile_id.strip())

                if tile_id != -1:
                    rect = pygame.Rect(
                        col_index * TILE_SIZE,
                        row_index * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    spike_rects.append(rect)

        return spike_rects