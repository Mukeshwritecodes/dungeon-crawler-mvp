from pydoc_data.topics import topics

import pygame
from config import WIDTH, HEIGHT
from utils.constants import TILE_SIZE


class Helper:
    def __init__(self):
        pass

    def load_image(self, path):
        image = pygame.image.load(path).convert_alpha()
        return image

    def load_animation(self, path):
        pass

