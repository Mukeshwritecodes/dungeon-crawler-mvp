import sys
import pygame
from core import game
game = game.Game()

pygame.init()
game.run()

# Uninitialize modules
pygame.quit()
sys.exit()