import pygame

SPEED = 300
dt = 0

playerPos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def movement_handler(event):
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        playerPos.y -= dt * SPEED
    if key[pygame.K_s]:
        playerPos.y += dt * SPEED
    if key[pygame.K_a]:
        playerPos.x -= dt * SPEED
    if key[pygame.K_d]:
        playerPos.x += dt * SPEED