import sys
import pygame
from core.game import Game
pygame.init()

game = Game()
game.run()


# Uninitialize modules
pygame.quit()
sys.exit()