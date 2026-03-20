from config import WIDTH, HEIGHT

class Camera:
    def __init__(self):
        pass

    @staticmethod
    def update_camera(player_rect, camera_pos):
        camera_x = player_rect.centerx - (WIDTH / 2)
        camera_y = player_rect.centery - (HEIGHT / 2)
        camera_pos.x = camera_x
        camera_pos.y = camera_y
        return camera_pos

