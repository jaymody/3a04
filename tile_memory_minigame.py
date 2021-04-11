# MODULE IMPORTS
import pygame # pylint: disable=import-error
import random
from pygame.color import Color
from itertools import product
from pygame.locals import *

# CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = SCREEN_WIDTH #includes functionality for non-square screen sizes
TILE_SIZE = 50
TILE_GAP = 10
FPS = 60

# board widths for each difficulty (1/2/3 = EASY/MEDIUM/HARD)
BOARD_WIDTH_1 = 3
BOARD_WIDTH_2 = 4
BOARD_WIFTH_3 = 5

BG_COLOR = Color('black')

# GLOBALS
board_width = 3
x_margin = (SCREEN_WIDTH - (board_width * (TILE_SIZE + TILE_GAP))) // 2
y_margin = (SCREEN_HEIGHT - (board_width * (TILE_SIZE + TILE_GAP))) // 2 

# checks if user has flipped all the correct tiles
def wincon(board, flipped):
    return board == flipped

# shows plays tiles 
def game_start_animation(board):
    """Lets player read minigame prompt, then flips tiles for 3 seconds and flips them back"""
    
    pygame.time.wait(3000)

    # all tiles to be memorized are flipped
    empty = [[False] * board_width] * board_width
    draw_board(board)
    pygame.time.wait(3000)
    draw_board(empty)

# setting up board
def generate_board():
    """ Generates random board given board width """
    
    tiles = board_width**2
    board = []
    #tiles to memorize (4 for 3x3, 7 for 4x4, 11 for 5x5, 16 for 6x6)
    for i in range(tiles * 4 //9):
        board.append([True])
    #blank tiles
    for i in range(tiles - (tiles * 4 //9)):
        board.append([False]) 
    #randomizes tile placement
    random.shuffle(board) 
    #converts 1D array of randomized True/False values (tiles) into 2D array
    board2D = [board[i:i + board_width] for i in range (0, board_width**2, board_width) ]

    return board2D

def get_coord(x, y):
    """ Gets the coordinates of particular tiles.
        The tiles are number height wise and then width wise.
        So the x and y are interchanged."""

    top = x_margin + y * (TILE_SIZE + TILE_GAP)
    left = y_margin + x * (TILE_SIZE + TILE_GAP)
    return top, left


def get_pos(cx, cy):
    """Gets the tile (x, y) position  from the cartesian coordinates.
       The tiles are number height wise and then width wise.
       So the cx and cy are interchanged."""

    if cx < x_margin or cy < y_margin:
        return None, None

    x = (cy - y_margin) // (TILE_SIZE + TILE_GAP)
    y = (cx - x_margin) // (TILE_SIZE + TILE_GAP)

    if x >= board_width or y >= board_width or(cx - x_margin) % (TILE_SIZE + TILE_GAP) > TILE_SIZE or (cy - y_margin) % (TILE_SIZE + TILE_GAP) > TILE_SIZE:
        return None, None
    else:
        return x, y

def draw_tile(flipped, x, y):
    """Draws a particular tile"""

    coords = get_coord(x, y)
    square_rect = (*coords, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, BG_COLOR, square_rect)
    if flipped[x][y]:
        pygame.draw.rect(screen, Color('blue'), square_rect)
    else:
        pygame.draw.rect(screen, Color('grey'), square_rect)
    pygame.display.update(square_rect)


def draw_board(flipped):
    """Draws the entire board"""

    for x in range(board_width):
        for y in range(board_width):
            draw_tile(flipped, x, y)


def draw_hover_box(x, y):
    """Draws the highlight box around the square"""

    px, py = get_coord(x, y)
    pygame.draw.rect(screen, Color('red'), (px - 5, py - 5, TILE_SIZE + 10, TILE_SIZE + 10), 5)


# main function
def main():
    global screen, clock

    # initialize
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
    else: #diff == 3
        board_width = BOARD_WIFTH_3

    #initialize margins
    x_margin = (SCREEN_WIDTH - (board_width * (TILE_SIZE + TILE_GAP))) // 2
    y_margin = (SCREEN_HEIGHT - (board_width * (TILE_SIZE + TILE_GAP))) // 2

    #generates random board
    board = generate_board()
    #all tiles start off unflipped
    flipped = [[False] * board_width] * board_width #tracks flipped tiles

    #mouse tracking variables
    mouse_x = None
    mouse_y = None
    mouse_clicked = False

    running = True

    game_start_animation(board)

    while running:
        screen.fill(BG_COLOR)
        draw_board(flipped)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_clicked = True

        x, y = get_pos(mouse_x, mouse_y)

        if x is not None and y is not None:
            if not flipped[x][y]:
                if mouse_clicked:
                    #flips tile and draws board
                    flipped[x][y] = True
                    draw_tile(board, flipped, x, y)
                    
                    if board[x][y]: #selected tile is correct
                        if wincon(board, flipped):
                            #game_won_animation(board, flipped)
                            running = False

                    else: #selected tile is wrong
                        pygame.time.wait(1500)
                        #flips over all tiles 
                        flipped = [[False] * board_width] * board_width
                        draw_tile(board, flipped, x, y)
                        pygame.time.wait(1000)

                else:
                    draw_hover_box(x, y)
        
        mouse_clicked = False
        pygame.display.update()
    
    else:
        pygame.quit()
        quit()

if __name__ == "__main__":
    main()