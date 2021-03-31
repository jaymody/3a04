"""Super Snakes and Ladders"""
import sys
import random

import pygame
import pygame_menu

from pygame import Rect, Surface

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)


def smooth_motion(t, b, c):
    """Computes points along a 1D line for a smooth accelerated/decelerated motion.

    Parameters
    ----------
    t : float
        Time t to compute distance at (0 <= t <= b)
    b : float
        Maximum time (ie, time needed to traverse the whole line), in other words
        smooth_motion(b) == c
        (b >= 0)
    c : float
        Length of the line (c >= 0)

    Returns
    -------
    float
        Distance d along the line at time t
    """
    # accelerate / decelerate motion
    # linear accelaration, quadratic speed, cubic distance
    # speed = -ax^2 + abx
    # distance = derivative of speed
    assert b >= 0
    assert c >= 0
    assert 0 <= t <= b
    a = 6 * c / b ** 3
    return -a / 3 * t ** 3 + a * b / 2 * t ** 2


class Game:
    def __init__(self, screen, clock, font, w, h, num_players):
        """Game instance of Super Snakes and Ladders

        Parameters
        ----------
        screen : pygame.display
            Game screen
        clock : pygame.clock
            Game clock
        font : pygame.font
            Game font
        w : int
            Width of screen
        h : int
            Height of screen
        num_players : int
            Number of players (2 <= num_players <= 4)
        """
        assert 2 <= num_players <= 4

        self.board = Board()
        self.screen = screen
        self.clock = clock
        self.font = font

        # generate pygame.Rect's for the board squares
        s = h // 12
        coords = list(map(self.board.get_coord, list(range(100))))
        self.squares = [Rect(s + c * s, h - 2 * s - r * s, s, s) for r, c in coords]

        # button/prompt
        self.button_roll = Rect(s * 12, s * 1, s * 4, s)
        self.box_prompt = Rect(s * 12, s * 3, s * 4, s * 4)
        self.prompt = ""

        # players[a] = b, such that a is the player number and b is
        # their position on the board
        self.players = [0] * num_players

        # turn represents the current player who has their turn
        self.turn = 0

        # start the game :D
        self.play_game()

    @property
    def p(self):
        """Current player number"""
        return self.turn

    @property
    def pos(self):
        """Current player's position"""
        return self.players[self.p]

    def animate(self, v1, v2, seconds=0.3, fps=30):
        """Animate the current player moving from point v1 to point v2

        Parameters
        ----------
        v1 : pygame.math.Vector2
            Source position
        v2 : pygame.math.Vector2
            Destination position
        seconds : float, optional
            Number of seconds the animation lasts, by default 0.3
        fps : int, optional
            Number of frames per second, by default 30
        """
        v3 = v2 - v1  # vector from old position (v1) to new position (v2)
        ticks = int(seconds * fps)  # number of ticks it will take to animate

        for t in range(ticks):
            scale = smooth_motion(t, ticks, ticks) / ticks  # scale v3 by this
            pos = (v1 + scale * v3).xy

            self.draw_board()
            self.draw_players(False)
            self.screen.blit(
                self.font.render(str(self.p + 1), True, black),
                pos,
            )
            pygame.display.update()

            self.clock.tick(fps)

    def move(self, n):
        """Move the current player n squares

        Parameters
        ----------
        n : int
            Number of square to move (move backwards if negative)
        """
        old_pos = self.pos
        new_pos = min(max(old_pos + n, 0), 99)  # make sure we don't go over/under
        self.players[self.p] = new_pos

        if n > 0:  # move forwards
            positions = list(range(old_pos, new_pos + 1))
        else:  # move backwards
            positions = list(range(old_pos, new_pos - 1, -1))

        for old, new in zip(positions[:-1], positions[1:]):
            v1 = pygame.math.Vector2(self.squares[old].center)
            v2 = pygame.math.Vector2(self.squares[new].center)
            self.animate(v1, v2)

    def snake(self):
        """Make the current player go down the snake"""
        self.prompt = f"P{self.p + 1} landed on a snake! Play a minigame."
        self.draw_board("Play Minigame")
        self.draw_players()
        pygame.display.update()
        self.wait_for_click()

        minigame_won = self.play_minigame()
        if minigame_won:
            self.prompt = f"P{self.p + 1} won the minigame and get's to stay put"
        else:
            self.prompt = f"P{self.p + 1} lost the minigame and slides down the snake"
            v2 = pygame.math.Vector2(self.squares[self.board.snakes[self.pos]].center)
            v1 = pygame.math.Vector2(self.squares[self.pos].center)
            self.animate(v1, v2, seconds=1)
            self.players[self.p] = self.board.snakes[self.pos]

    def ladder(self):
        """Make the current player go up the ladder"""
        self.prompt = f"P{self.p + 1} has landed on a ladder! Play a minigame."
        self.draw_board("Play Minigame")
        self.draw_players()
        pygame.display.update()
        self.wait_for_click()

        minigame_won = self.play_minigame()
        if minigame_won:
            self.prompt = (
                f"P{self.p + 1} won the minigame and get's to climb the ladder"
            )
            v1 = pygame.math.Vector2(self.squares[self.pos].center)
            v2 = pygame.math.Vector2(self.squares[self.board.ladders[self.pos]].center)
            self.animate(v1, v2, seconds=1)
            self.players[self.p] = self.board.ladders[self.pos]
        else:
            self.prompt = f"P{self.p + 1} lost the minigame and has to stay put"

    def draw_board(self, button_text="Roll"):
        """Draw the board, buttons, and prompt

        Parameters
        ----------
        button_text : str, optional
            Text for the button, by default "Roll"

        Note
        ----
        pygame.display.update() needs to be called to update the screen.
        self.prompt determines the text to be drawn for the prompt.
        """
        # draw background (draws over everything, acts as a screen clear)
        self.screen.fill(white)

        # draw the button
        pygame.draw.rect(self.screen, blue, self.button_roll)
        self.screen.blit(
            self.font.render(button_text, True, white), self.button_roll.center
        )

        # draw the prompt
        self.screen.blit(
            self.font.render(self.prompt, True, black), self.box_prompt.topleft
        )

        # draw the squares
        for i, sq in enumerate(self.squares):
            pygame.draw.rect(self.screen, black, sq, width=3)
            self.screen.blit(self.font.render(str(i + 1), True, black), sq.topleft)

        # draw the snakes
        for start, end in self.board.snakes.items():
            pygame.draw.line(
                self.screen,
                green,
                self.squares[start].center,
                self.squares[end].center,
                width=4,
            )

        # draw the ladders
        for start, end in self.board.ladders.items():
            pygame.draw.line(
                self.screen,
                red,
                self.squares[start].center,
                self.squares[end].center,
                width=4,
            )

        # draw the special squares
        for pos in self.board.special:
            pygame.draw.circle(
                self.screen,
                blue,
                self.squares[pos].center,
                radius=4,
            )

    def draw_players(self, draw_current_player=True):
        """Draw the players on the board

        Parameters
        ----------
        draw_current_player : bool, optional
            Draw the current player, by default True
        """
        for p, player in enumerate(self.players):
            if not draw_current_player and p == self.p:
                continue
            self.screen.blit(
                self.font.render(str(p + 1), True, black),
                self.squares[player].center,
            )

    def wait_for_click(self):
        """Wait for user to click the button."""
        while True:
            pygame.event.clear()
            event = pygame.event.wait()
            if event.type == pygame.QUIT or event.type == 32787:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_roll.collidepoint(event.pos):
                    return

    def roll(self):
        """Simulate dice roll."""
        return random.randint(1, 6)

    def play_minigame(self, pos=None):
        """Start a new minigame

        Parameters
        ----------
        pos : int
            Position of player. Used to determine difficulty.

        Returns
        -------
        bool
            True if the minigame was won, else False
        """
        # TODO: implement this
        return random.random() > 0.5

    def play_turn(self, backwards=False):
        """Turn logic

        Parameters
        ----------
        backwards : bool, optional
            Whether the roll should make the player go backwards, by default False

        Returns
        -------
        bool
            True if the player has won the game, else False
        """
        p = self.turn  # assign turn to p, just makes things easier to read

        self.wait_for_click()  # wait for player to press roll
        n = self.roll()
        if backwards:
            n = -n
        self.prompt = f"P{p + 1} rolled a {n}"
        self.move(n)

        if self.pos >= 99:  # they've won the game
            return True

        # determines if current square is snake/ladder/special
        square = self.board.get_square(self.pos)

        # check if we landed on an action square (square will be None if it's
        # a normal square and not a snake/ladder/special square)
        if square is not None:
            if square == self.board.SNAKE_SQUARE:
                self.snake()
            elif square == self.board.LADDER_SQUARE:
                self.ladder()
            elif square == self.board.SPECIAL_SQUARE:
                self.prompt = (
                    f"P{self.p + 1} landed on a special square! Play a minigame."
                )
                self.draw_board("Play Minigame")
                self.draw_players()
                pygame.display.update()
                self.wait_for_click()

                minigame_won = self.play_minigame()
                if minigame_won:
                    self.prompt = f"P{self.p + 1} won the minigame and get's to roll again to go forwards"
                else:
                    self.prompt = f"P{self.p + 1} lost the minigame and has to roll again to go backwards"

                self.draw_board()
                self.draw_players()
                pygame.display.update()
                return self.play_turn(backwards=not minigame_won)

        return False

    def play_game(self):
        """Main game loop"""
        self.prompt = f"P{(self.turn % len(self.players)) + 1}'s turn"
        self.draw_board()
        self.draw_players()
        pygame.display.update()
        while True:
            game_won = self.play_turn()
            if game_won:
                print(f"P{self.turn} WON")
                return
            self.turn = (self.turn + 1) % len(self.players)
            self.prompt += f", P{(self.turn % len(self.players)) + 1}'s turn"
            self.draw_board()
            self.draw_players()
            pygame.display.update()


class Board:
    SNAKE_SQUARE = 0
    LADDER_SQUARE = 1
    SPECIAL_SQUARE = 2

    def __init__(
        self,
        snakes={96: 77, 94: 55, 87: 23, 61: 17, 47: 25, 35: 5, 31: 9},
        ladders={1: 37, 3: 13, 7: 29, 27: 73, 20: 41, 49: 66, 70: 91, 79: 98},
        nspecial=5,
    ):
        """Game board

        The board contains positions from 0 (start, bottom left) to 99 (end, top left)

        Parameters
        ----------
        snakes : dict, optional
            Head positions -> tail positions
        ladders : dict, optional
            Bottom bottom -> top position
        nspecial : int, optional
            Number of special squares to generate, by default 5
        """
        for k, v in snakes.items():
            assert 0 < k < 99 and 0 < v < 99

        for k, v in ladders.items():
            assert 0 < k < 99 and 0 < v < 99

        assert len(snakes) < 10 and len(ladders) < 10 and nspecial < 10

        self.snakes = snakes
        self.ladders = ladders

        # generate nspecial random positions for the special squares
        # don't include square 0 or square 99 or squares used by snakes/ladders
        used_squares = (
            set(self.snakes.keys())
            | set(self.ladders.keys())
            | set(self.snakes.values())
            | set(self.ladders.values())
        )
        unused_squares = set(range(1, 99)) - used_squares
        self.special = random.sample(unused_squares, nspecial)

    def get_coord(self, pos):
        """Get row and col of a give position

        Parameters
        ----------
        pos : int
            Position

        Returns
        -------
        int, int
            Row and column
        """
        row = pos // 10
        col = pos % 10 if row % 2 == 0 else (9 - pos % 10)
        return row, col

    def get_square(self, pos):
        """Get type of square at a given position (None if it is "normal")

        Parameters
        ----------
        pos : int
            Position

        Returns
        -------
        int or None
            Type of square at pos
        """
        if pos in self.snakes:
            return self.SNAKE_SQUARE
        elif pos in self.ladders:
            return self.LADDER_SQUARE
        elif pos in self.special:
            return self.SPECIAL_SQUARE
        else:
            return None


if __name__ == "__main__":
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
        "Play", lambda: Game(screen, clock, font, w=width, h=height, num_players=2)
    )
    menu.add.button("Help", help_menu)
    menu.add.button("Settings", settings_menu)
    menu.add.button("Quit", pygame_menu.events.EXIT)
    menu.mainloop(screen)
