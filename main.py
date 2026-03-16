import sys
import pygame

pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

running = True

# Loop until 'X' is pressed
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    screen.fill((0, 0, 0))

    # Update screen in each iteration
    pygame.display.flip()

# Uninitialize modules
pygame.quit()
sys.exit()