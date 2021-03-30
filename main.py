import random

import pygame
import pygame_menu

from pygame import Rect, Surface


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)


class Game:
    def __init__(self, screen, w, h, num_players):
        """Initialize a new game."""
        self.board = Board()

        self.screen = screen

        s = h // 12
        coords = list(map(self.board.get_coord, list(range(95))))
        self.squares = [Rect(s + c * s, h - 2 * s - r * s, s, s) for r, c in coords]

        self.players = [0] * num_players
        self.turn = 0

        self.play_game()

    def roll(self):
        return random.randint(1, 6)

    def start_minigame(self):
        # TODO: implement this
        return random.random() > 0.5

    def display_board(self):
        # each square is about 80 pixels
        # draw_snake = lambda x, y: pygame.draw.line(self.screen)
        self.screen.fill(white)

        for sq in self.squares:
            pygame.draw.rect(self.screen, black, sq)

    def animate_move(self):
        pass

    def animate_snake(self):
        pass

    def animate_ladder(self):
        pass

    def animate_roll(self):
        pass

    def play_turn(self, p, backwards=False):
        """Runs a turn for the

        Parameters
        ----------
        p : int
            Player number.

        Returns
        -------
        bool
            True if the p has won.
        """

        # increments current player pos by dice roll
        # TODO: let player hit the roll button
        if backwards:
            self.players[p] -= self.roll()
        else:
            self.players[p] += self.roll()

        if self.players[p] >= 99:
            # they've won the game
            return True

        # determines if current square is snake/ladder/special
        square = self.board.get_square(self.players[p])

        # different squares
        sq_snake = self.board.SNAKE_SQUARE
        sq_ladder = self.board.LADDER_SQUARE
        sq_special = self.board.SPECIAL_SQUARE

        if square == sq_snake:
            minigame_won = self.start_minigame()
            if not minigame_won:
                self.players[p] = self.board.snakes[self.players[p]]
        elif square == sq_ladder:
            minigame_won = self.start_minigame()
            if minigame_won:
                self.players[p] = self.board.ladders[self.players[p]]
        elif square == sq_special:
            minigame_won = self.start_minigame()
            if minigame_won:
                return self.play_turn(p)
            else:
                return self.play_turn(p, backwards=True)
        else:
            return False

    def play_game(self):
        """Main game loop."""
        self.display_board()
        pygame.display.update()

        while True:
            print(self.players)
            if self.play_turn(self.turn % len(self.players)):
                print(f"p {(self.turn %  len(self.players))+1} WON")
                break
            self.turn += 1


class Board:
    SNAKE_SQUARE = 0
    LADDER_SQUARE = 1
    SPECIAL_SQUARE = 2

    def __init__(self):
        """Board constructor."""
        # {head:tail, bottomladder:topladder, etc}
        # snake heads call minigame
        self.snakes = {96: 77, 94: 55, 87: 23, 61: 17, 47: 25, 35: 5, 31: 9}
        # ladder bottoms call minigame, LADDER MUST NOT GO DIRECTLY TO WIN
        self.ladders = {1: 37, 3: 13, 7: 29, 27: 73, 20: 41, 49: 66, 70: 91, 79: 98}

        # generate 5 random positions for the special squares
        # don't include square 0 or square 99\
        used_squares = set(self.snakes.keys()) | set(self.ladders.keys())
        unused_squares = set(range(1, 99)) - used_squares
        self.special = random.sample(unused_squares, 5)

    def get_coord(self, pos):
        """Get coordinate on board (row, column) from bottom to top.

        Parameters
        ----------
        pos : int
            Position from 0 to 99.

        Returns
        -------
        row, col : int, int
            Integer pair containing row and column of the position. Row 0 is
            bottom most row, column 0 is leftmost row.
        """
        row = pos // 10
        col = pos % 10
        return row, col

    def get_square(self, pos):
        """Gets if a position is on a snake/ladder/special/normal square."""

        if pos in self.snakes:
            return self.SNAKE_SQUARE
        elif pos in self.ladders:
            return self.LADDER_SQUARE
        elif pos in self.special:
            return self.SPECIAL_SQUARE
        else:
            return None


if __name__ == "__main__":
    width = 1280
    height = 720
    theme = pygame_menu.themes.THEME_SOLARIZED

    pygame.init()
    # pygame.font.init()
    # Font = pygame.font.SysFont("comicsans", 20)
    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption("Super Snakes and Ladders")
    clock = pygame.time.Clock()

    # add icon, add sprite, add better colors

    # help menu
    help_menu = pygame_menu.Menu("Instructions", width, height, theme=theme)

    help_menu.add.button("Back", pygame_menu.events.RESET)

    # settings menu
    settings_menu = pygame_menu.Menu("Settings", width, height, theme=theme)
    settings_menu.add.button("Back", pygame_menu.events.RESET)

    # main menu
    menu = pygame_menu.Menu("Super Snakes and Ladders", width, height, theme=theme)
    menu.add.button("Play", lambda: Game(screen, w=width, h=height, num_players=2))
    menu.add.button("Help", help_menu)
    menu.add.button("Settings", settings_menu)
    menu.add.button("Quit", pygame_menu.events.EXIT)
    menu.mainloop(screen)
