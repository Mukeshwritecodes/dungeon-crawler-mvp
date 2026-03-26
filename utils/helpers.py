from pydoc_data.topics import topics
import pygame


class Helper:
    def __init__(self):
        pass

    # Loads image from the given path
    def load_image(self, path):
        image = pygame.image.load(path).convert_alpha()
        return image

    # Load sprite list from the given path of the spritesheet
    def load_sprites(self, path, sprite_width):
        spritesheet = self.load_image(path)
        x = 0
        y = 0
        sprites = []
        cols = int(spritesheet.width / sprite_width)
        for i in range(cols):
            rect = pygame.Rect(x, y, sprite_width, spritesheet.get_height())
            sprites.append(spritesheet.subsurface(rect))
            x += sprite_width
        return sprites


