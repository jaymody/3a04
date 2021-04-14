import pygame
import sys
import os
import time
import random
from pygame.color import Color
from itertools import product
from pygame.locals import *

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

# CONSTANTS
TILE_SIZE = 50
TILE_GAP = 10
BG_COLOR = Color('black')

class TileMemory:
    def __init__(self, difficulty, screen, clock, font, w, h, fps):
        self.difficulty = difficulty
        self.screen = screen
        self.clock = clock
        self.font = font
        self.w, self.h = w, h
        self.fps = fps

        #changes board size based on difficulty
        if self.difficulty == "easy":
            self.board_width = 3
        elif self.difficulty == "medium":
            self.board_width = 4
        else: #self.difficulty == "hard"
            self.board_width = 5

        #margins for mouse tracking calculations
        self.x_margin = (self.w - (self.board_width * (TILE_SIZE + TILE_GAP))) // 2
        self.y_margin = (self.h - (self.board_width * (TILE_SIZE + TILE_GAP))) // 2 

    def wincon(self, board, flipped):
        """ Win condition: player has flipped all the correct tiles """
        return board == flipped
 
    def game_start_animation(self, board):
        """ Three seconds to read minigame prompt
            Three seconds to view and memorize tiles
            Flips back tiles """
        
        # all tiles to be memorized are flipped

        self.screen.fill(BG_COLOR)

        empty = [[False]*self.board_width for _ in range(self.board_width)]
        self.draw_board(empty)
        pygame.time.wait(3000)
        self.draw_board(board)
        pygame.time.wait(2000)
        self.draw_board(empty)

    def generate_board(self):
        """ Generates random board given board width """
        
        tiles = self.board_width**2
        board = []

        #tiles to memorize (4 for 3x3, 7 for 4x4, 11 for 5x5, 16 for 6x6)
        for i in range(tiles * 4 //9):
            board.append(True)
        #blank tiles
        for i in range(tiles - (tiles * 4 //9)):
            board.append(False)
        
        #randomizes tile placement
        random.shuffle(board)

        #converts 1D array of randomized True/False values (tiles) into 2D array
        board2D = [board[i:i + self.board_width] for i in range (0, self.board_width**2, self.board_width)]

        return board2D

    def get_coord(self, x, y):
        """ Gets the coordinates of particular tiles
            The tiles are number height wise and then width wise
            So the x and y are interchanged """

        top = self.x_margin + y * (TILE_SIZE + TILE_GAP)
        left = self.y_margin + x * (TILE_SIZE + TILE_GAP)
        return top, left

    def get_pos(self, cx, cy):
        """Gets the tile (x, y) position  from the cartesian coordinates
        The tiles are number height wise and then width wise 
        So the cx and cy are interchanged """

        if cx < self.x_margin or cy < self.y_margin:
            return None, None

        x = (cy - self.y_margin) // (TILE_SIZE + TILE_GAP)
        y = (cx - self.x_margin) // (TILE_SIZE + TILE_GAP)

        if x >= self.board_width or y >= self.board_width or(cx - self.x_margin) % (TILE_SIZE + TILE_GAP) > TILE_SIZE or (cy - self.y_margin) % (TILE_SIZE + TILE_GAP) > TILE_SIZE:
            return None, None
        else:
            return x, y

    def draw_tile(self, flipped, x, y, update=True):
        """ Draws a particular tile """

        coords = self.get_coord(x, y)
        square_rect = (*coords, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.screen, BG_COLOR, square_rect)
        if flipped[x][y]:
            pygame.draw.rect(self.screen, Color('blue'), square_rect)
        else:
            pygame.draw.rect(self.screen, Color('grey'), square_rect)

        if update:
            pygame.display.update(square_rect)

    def draw_board(self, flipped):
        """ Draws the entire board """

        for x in range(self.board_width):
            for y in range(self.board_width):
                self.draw_tile(flipped, x, y, update=False)
        pygame.display.update()

    def draw_hover_box(self, x, y):
        """ Draws the highlight box around the square """

        px, py = self.get_coord(x, y)
        pygame.draw.rect(self.screen, Color('red'), (px - 5, py - 5, TILE_SIZE + 10, TILE_SIZE + 10), 5)
    
    def play_minigame(self):
        """ Returns True if minigame is won, False if lost """

        #initialize margins
        self.x_margin = (self.w - (self.board_width * (TILE_SIZE + TILE_GAP))) // 2
        self.y_margin = (self.h - (self.board_width * (TILE_SIZE + TILE_GAP))) // 2

        #generates random board
        board = self.generate_board()
        #all tiles start off unflipped
        flipped = [[False]*self.board_width for _ in range(self.board_width)]

        #mouse tracking variables
        mouse_x = None
        mouse_y = None
        mouse_clicked = False

        running = True

        self.game_start_animation(board)

        while running:
            self.screen.fill(BG_COLOR)
            self.draw_board(flipped)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_clicked = True

            x, y = self.get_pos(mouse_x, mouse_y)

            if x is not None and y is not None:
                if not flipped[x][y]:
                    if mouse_clicked:
                        #flips tile and draws board
                        flipped[x][y] = True
                        self.draw_tile(flipped, x, y)
                        
                        #selected tile is correct
                        if board[x][y]: 
                            if self.wincon(board, flipped):
                                #game_won_animation(board, flipped)
                                return True
                        
                        #selected tile is wrong
                        else: 
                            pygame.time.wait(1500)
                            #flips over all tiles
                            #game_lose_animation(board, flipped)
                            flipped = [[False]*self.board_width for _ in range(self.board_width)]
                            self.draw_board(flipped)
                            pygame.time.wait(1000)
                            return False

                    else:
                        self.draw_hover_box(x, y)
            
            mouse_clicked = False
            pygame.display.update()
        
        else:
            pygame.quit()
            quit()


if __name__ == "__main__":
    # constants
    width = 1280
    height = 720
    fps = 60

    # initialize
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("timesnewroman", 20)
    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption("Tile Memory Minigame")
    clock = pygame.time.Clock()

    # start game
    minigame = TileMemory("hard", screen, clock, font, width, height, fps)
    result = minigame.play_minigame()
    print(f"\n\nGame Result: {result}")
