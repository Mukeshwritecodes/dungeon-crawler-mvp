import pygame

class InputHandler:
    def movement_handler(self, events):
        actions = []
        key = pygame.key.get_pressed()
        if key[pygame.K_w] or key[pygame.K_SPACE] or key[pygame.K_UP]:
            actions.append("JUMP")
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            actions.append("DOWN")
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            actions.append("RIGHT")
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            actions.append("LEFT")
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    actions.append("TRANSFORM")
                if event.key == pygame.K_q:
                    actions.append("ATTACK")

        return actions