import pygame
import colours
import sys


# TODO:
# 1. SETUP THE GRID
# > create a window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
GREEN = (173, 216, 230)

pygame.init()
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minesweeper")
surface.fill(colours.BLUE)


# create mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            pygame.quit()
            sys.exit()
    pygame.display.update()
# 2. EACH TILE ON THE GRID IS A BUTTON AT FIRST
# 3. OKAY