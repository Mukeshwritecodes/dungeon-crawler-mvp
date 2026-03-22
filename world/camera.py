import pygame

from config import WIDTH, HEIGHT

class Camera:
    def __init__(self):
        pass

    @staticmethod
    def update_camera(player_rect, camera_pos):
        camera_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        map_rect = pygame.Rect(-200, 0, 100*32, 120*32)

        # Subtracting the center of the screen from the center of the player
        camera_x = player_rect.centerx - (WIDTH / 2)
        camera_y = player_rect.centery - (HEIGHT / 2)

        camera_pos.x = camera_x # X offset
        camera_pos.y = camera_y # Y offset

        # Clamps the camera so that the boundary outside the map isn't visible
        camera_rect.topleft = (camera_pos.x, camera_pos.y)
        camera_rect.clamp_ip(map_rect)
        return camera_rect

