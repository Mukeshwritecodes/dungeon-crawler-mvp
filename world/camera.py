import pygame

from config import WIDTH, HEIGHT

class Camera:
    def __init__(self):
        pass

    @staticmethod
    def update_camera(player_rect, camera_pos, smoothness=10):
        # 1. Define your map boundaries
        map_rect = pygame.Rect(-200, 0, 100 * 32, 120 * 32)

        # 2. Calculate where the camera SHOULD be (the Target)
        target_x = player_rect.centerx - (WIDTH / 2)
        target_y = player_rect.centery - (HEIGHT / 2)

        # 3. Smoothing Logic (LERP)
        # Move the current position towards the target by 1/smoothness of the distance
        camera_pos.x += (target_x - camera_pos.x) / smoothness
        camera_pos.y += (target_y - camera_pos.y) / smoothness

        # 4. Clamping (ensures the camera doesn't show the void)
        camera_rect = pygame.Rect(camera_pos.x, camera_pos.y, WIDTH, HEIGHT)
        camera_rect.clamp_ip(map_rect)

        return camera_rect

