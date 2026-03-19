import pygame

class InputHandler:
    def movement_handler(self):
        actions = []
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            actions.append("JUMP")
        #if key[pygame.K_DOWN]:
         #   actions.append("CROUCH")
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            actions.append("RIGHT")
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            actions.append("LEFT")

        return actions