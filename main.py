"""Super Snakes and Ladders"""
import sys

import pygame
import pygame_menu

from game import Game


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
    fps = 30
    theme = pygame_menu.themes.THEME_SOLARIZED

    # initialize
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("timesnewroman", 20)
    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption("Super Snakes and Ladders")
    clock = pygame.time.Clock()

    # help menu
    help_menu = pygame_menu.Menu("Instructions", width, height, theme=theme)
    help_menu.add.button("Back", pygame_menu.events.RESET)

    # settings menu
    settings_menu = pygame_menu.Menu("Settings", width, height, theme=theme)
    settings_menu.add.button("Back", pygame_menu.events.RESET)

    # main menu
    menu = pygame_menu.Menu("Super Snakes and Ladders", width, height, theme=theme)
    menu.add.button(
        "Play",
        lambda: Game(screen, clock, font, w=width, h=height, fps=fps, num_players=2),
    )
    menu.add.button("Help", help_menu)
    menu.add.button("Settings", settings_menu)
    menu.add.button("Quit", pygame_menu.events.EXIT)
    menu.mainloop(screen)


if __name__ == "__main__":
    main()
