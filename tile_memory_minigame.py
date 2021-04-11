# MODULE IMPORTS
import pygame # pylint: disable=import-error
import random
#from itertools import product
#from pygame.locals import *
# from pygame.color import COlor

# CONSTANTS
SCREEN_WIDTH = 800
#SCREEN_HEIGHT = 800 #unecessary variable given square window size
TILE_SIZE = 50
TILE_GAPS = 10

# board widths for each difficulty (1/2/3 = EASY/MEDIUM/HARD)
BOARD_WIDTH_1 = 4
BOARD_WIDTH_2 = 5
BOARD_WIFTH_3 = 6

#margins for each board width?
# MARGIN_1 = 
# MARGIN_2 = 
# MARGIN_3 = 


# MAIN FUNCTION
def main():
    global screen, clock

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
    pygame.display.set_caption("Tile Memory Minigame")

    

if __name__ == "__main__":
    main()