import pygame
#SPEED = 300
#dt = 0
action = []

class InputHandler():
    def movement_handler(self, event):
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            action.append("JUMP")
        if key[pygame.K_DOWN]:
            action.append("CROUCH")
        if key[pygame.K_a] or key[pygame.K_RIGHT]:
            action.append("RIGHT")
        if key[pygame.K_d] or key[pygame.K_LEFT]:
            action.append("LEFT")

        return action