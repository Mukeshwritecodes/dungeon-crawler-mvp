import pygame

from config import WIDTH, HEIGHT


class UISystem:
    def __init__(self):
        self.font_small = pygame.font.SysFont(None, 24)
        self.font_large = pygame.font.SysFont(None, 40)

    def draw_hud(self, screen, player):
        self.draw_health_bar(screen, player)
        self.draw_xp_bar(screen, player)
        self.draw_level(screen, player)

    def draw_health_bar(self, screen, player):
        max_width = 200
        height = 15
        x, y = 20, 20

        if not player.is_alive:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, 0, height))
            pygame.draw.rect(screen, (255, 255, 255), (x, y, max_width, height), 2)
        else:
            ratio = player.health / player.max_health
            pygame.draw.rect(screen, (255, 0, 0), (x, y, max_width * ratio, height))
            pygame.draw.rect(screen, (255, 255, 255), (x, y, max_width, height), 2)

    def draw_xp_bar(self, screen, player):
        max_width = 200
        height = 10
        x, y = 20, 40

        ratio = player.xp / player.level_xp
        pygame.draw.rect(screen, (0, 0, 255), (x, y, max_width * ratio, height))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, max_width, height), 2)

    def draw_level(self, screen, player):
        text = self.font_small.render(f"Level: {player.level}", True, (255, 255, 255))
        screen.blit(text, (20, 60))

    def draw_pause(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        text = self.font_large.render("PAUSED", True, (255, 255, 255))
        screen.blit(text, ((WIDTH // 2) - 80, (HEIGHT // 2) - 100))

    def draw_menu(self, screen):
        screen.fill((0, 0, 0))

        title = self.font_large.render("Shapebound", True, (255, 255, 255))
        start = self.font_small.render("Press ENTER to Start", True, (255, 255, 255))

        screen.blit(title, ((WIDTH // 2) - 100, (HEIGHT // 2) - 100))
        screen.blit(start, ((WIDTH // 2) - 100, HEIGHT // 2))