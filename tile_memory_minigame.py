# MODULE IMPORTS
import pygame # pylint: disable=import-error
import random
#from itertools import product
#from pygame.locals import *
# from pygame.color import Color

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



def game_start_animation(board):
    """Lets player read minigame prompt, then flips tiles for 3 seconds and flips them back"""
    

# setting up board
def generate_board(board_width):
    """ Generates random board given board width """
    
    tiles = board_width**2
    board = []
    board.append([True]*(tiles/2)) #tiles to memorize (half the tiles on each board size need to be memorized)
    board.append([False]*(tiles - tiles/2)) #blank tiles
    random.shuffle(board) #randomizes tile placement

    return board

def draw_square(board, flipped, x, y):



def draw_board(board, flipped):



def draw_hover_box(x, y):



def get_coords(x, y):



def get_pos(cx, cy):





# main function
def main():
    global screen, clock

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
    pygame.display.set_caption("Tile Memory Minigame")
    clock = pygame.time.Clock()

    #setting default difficulty to easy
    # figure out how to access difficulty parameter from game.py
    diff = 1

    #changes board size based on difficulty
    if diff == 1:
        board_width = BOARD_WIDTH_1
    elif diff == 2:
        board_width = BOARD_WIDTH_2
    else #diff == 3:
        board_width = BOARD_WIFTH_3

    board = generate_board(board_width)
    flipped = [[False] * board_width for i in range(board_width)]

    mouse_x = None
    mouse_y = None
    mouse_clicked = False


if __name__ == "__main__":
    main()