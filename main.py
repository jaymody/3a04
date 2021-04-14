"""Super Snakes and Ladders"""
import sys

import pygame
import pygame_menu
from pygame.locals import *
from game import Board
from game import Game

RICH_BLACK = (26, 27, 41)
AZURE = (230, 250, 252)
EMERALD = (47, 191, 113)
PRINCETON_ORANGE = (237, 125, 58)
ORANGE = (247, 149, 27)
RED = (239, 45, 86)
BG = (239, 231, 211)
PINKISH = (207, 62, 132)

alarm = pygame.image.load('./images/alarm.png')
bell = pygame.image.load('./images/bell.png')
compass = pygame.image.load('./images/compass.png')
culture = pygame.image.load('./images/culture.png')
drop = pygame.image.load('./images/drop.png')
gym = pygame.image.load('./images/gym.png')
lock = pygame.image.load('./images/lock.png')
plane = pygame.image.load('./images/plane.png')
pin = pygame.image.load('./images/pin.png')
smile = pygame.image.load('./images/smile.png')
trash = pygame.image.load('./images/trash.png')

def draw_text(text, font, color, screen, x, y, center=True):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    screen.blit(textobj, textrect)

class Instructions:
    def __init__(self, screen, clock, font, w, h):
        running = True
        click = False

        p1 = pygame.image.load('./assets/instructions/p1.png')
        p2 = pygame.image.load('./assets/instructions/p2.png')
        p3 = pygame.image.load('./assets/instructions/p3.png')
        p4 = pygame.image.load('./assets/instructions/p4.png')
        p5 = pygame.image.load('./assets/instructions/p5.png')
        p6 = pygame.image.load('./assets/instructions/p6.png')
        p7 = pygame.image.load('./assets/instructions/p7.png')

        instructions = [p1, p2, p3, p4, p5, p6, p7]
        index = 0

        while running:
            clock.tick(60)
    
            screen.blit(instructions[index], (0, 0))
           
            mx, my = pygame.mouse.get_pos()

            back_button = pygame.Rect(50, 100, 100, 40)
            back_button.center = (w/18, h/20)

            prev_button = pygame.Rect(50, 100, 100, 40)
            prev_button.center = (w/5*2, h/25*24)

            next_button = pygame.Rect(50, 100, 100, 40)
            next_button.center = (w/5*3, h/25*24)

            if back_button.collidepoint((mx, my)):
                if click:
                    running = False
                    break
            if prev_button.collidepoint((mx, my)):
                if click:
                    index -= 1
                    if index < 0:
                        index = len(instructions) - 1
            if next_button.collidepoint((mx, my)):
                if click:
                    index += 1
                    if index > len(instructions) - 1:
                        index = 0

            click = False

            pygame.draw.rect(screen, PINKISH, back_button, 1)
            draw_text('Back', font, PINKISH, screen, w/18, h/20)

            pygame.draw.rect(screen, PINKISH, prev_button, 1)
            draw_text('Prev', font, PINKISH, screen, w/5*2, h/25*24)

            pygame.draw.rect(screen, PINKISH, next_button, 1)
            draw_text('Next', font, PINKISH, screen, w/5*3, h/25*24)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            
            pygame.display.update()

def main():
    # TODO: game icon, themeing
    # TODO: minigames
    # TODO: settings menu
    # TODO: help menu
    # TODO: pictures/sound/sprites
    # TODO: game win screen

    # constants
    width = 1280
    height = 720
    theme = pygame_menu.themes.THEME_SOLARIZED

    # initialize
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 28)
    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption("Super Snakes and Ladders")
    clock = pygame.time.Clock()

    # settings menu
    board_1 = Board({96: 77, 94: 55, 87: 23, 61: 17, 47: 25, 35: 5, 31: 9}, {1: 37, 3: 13, 7: 29, 27: 73, 20: 41, 49: 66, 70: 91, 79: 98}, 7)
    board_2 = Board({16: 6, 61: 19, 86: 23, 53: 31, 63: 59, 92: 72, 97: 78, 94: 49}, {3: 13, 8: 30, 27: 83, 20: 41, 1: 37, 50: 66, 70: 90, 55: 77}, 9)
    board_3 = Board({46: 4, 29: 8, 37: 14, 96: 24, 61: 36, 85: 53, 91: 69, 52: 32}, {80: 98, 84: 94, 73: 87, 40: 78, 19: 76, 31: 67, 7: 33, 1: 22}, 7)
    board_pool = [("Board 1", board_1), ("Board 2", board_2), ("Board 3", board_3)]
    icon_pool = [("Alarm", alarm), ("Bell", bell), ("Compass", compass), ("Culture", culture), ("Drop", drop), ("Gym", gym), ("Lock", lock), ("Plane", plane), ("Pin", pin), ("Smile", smile), ("Trash", trash)]
    fps_pool = [("30", 30), ("60", 60), ("144", 144)]

    settings_menu = pygame_menu.Menu("Settings", width, height, theme=theme)
    board_selector = settings_menu.add.selector(
        title='Board:',
        items=board_pool,
        style=pygame_menu.widgets.SELECTOR_STYLE_FANCY
    )
    p1_icon_selector = settings_menu.add.selector(
        title='Player 1:',
        items=icon_pool,
        style=pygame_menu.widgets.SELECTOR_STYLE_FANCY
    )
    p2_icon_selector = settings_menu.add.selector(
        title='Player 2:',
        items=icon_pool,
        default=1,
        style=pygame_menu.widgets.SELECTOR_STYLE_FANCY
    )
    settings_menu.add.button("Back", pygame_menu.events.RESET)

    # main menu
    menu = pygame_menu.Menu("Super Snakes and Ladders", width, height, theme=theme)
    menu.add.button(
        "Play",
        lambda: Game(screen, clock, font, w=width, h=height, fps=60, num_players=2,
        player_icons=[p1_icon_selector.get_value()[0][1], p2_icon_selector.get_value()[0][1]], board=board_selector.get_value()[0][1]),
    )
    menu.add.button("Help", lambda: Instructions(screen, clock, font, width, height))
    menu.add.button("Settings", settings_menu)
    menu.add.button("Quit", pygame_menu.events.EXIT)
    menu.mainloop(screen)

if __name__ == "__main__":
    main()
