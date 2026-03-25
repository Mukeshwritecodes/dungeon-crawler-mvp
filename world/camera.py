import pygame

from config import WIDTH, HEIGHT
from utils.constants import TILE_SIZE


class Camera:
    def __init__(self):
        pass

    @staticmethod
    def update_camera(player_rect, camera_pos, smoothness=10):
        map_width = 120 * TILE_SIZE
        map_height = 45 * TILE_SIZE

        # Target (center player)
        target_x = player_rect.centerx - WIDTH / 2
        target_y = player_rect.centery - HEIGHT / 2

        # Smooth follow
        camera_pos.x += (target_x - camera_pos.x) / smoothness
        camera_pos.y += (target_y - camera_pos.y) / smoothness

        # 🔥 Clamp correctly
        #camera_pos.x = max(0, min(camera_pos.x, map_width - WIDTH))
        #camera_pos.y = max(0, min(camera_pos.y, map_height - HEIGHT))

        return pygame.Rect(int(camera_pos.x), int(camera_pos.y), WIDTH, HEIGHT)

