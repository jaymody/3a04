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

# click for minigame
# add game update text
# add animations


def cubic_distance(x, b, c):
    # accelerate / decelerate motion
    # linear accelaration, quadratic speed, cubic distance
    # speed = -ax^2 + abx
    # x = time
    # b = time needed to reach final position (max time)
    # c = final position
    assert b >= 0
    assert c >= 0
    assert x >= 0
    assert x <= b
    a = 6 * c / b ** 3
    return -a / 3 * x ** 3 + a * b / 2 * x ** 2


class Game:
    def __init__(self, screen, clock, font, w, h, num_players):
        self.board = Board()

        self.screen = screen
        self.clock = clock
        self.font = font

        s = h // 12
        coords = list(map(self.board.get_coord, list(range(100))))
        self.squares = [Rect(s + c * s, h - 2 * s - r * s, s, s) for r, c in coords]

        self.button_roll = Rect(s * 12, s * 1, s * 4, s)
        self.prompt_location = Rect(s * 12, s * 3, s * 4, s * 4).center
        self.prompt = ""

        self.w, self.h, self.s = w, h, s

        self.players = [0] * num_players
        self.turn = 0

        self.play_game()

    def roll(self):
        return random.randint(1, 6)

    def play_minigame(self):
        # TODO: implement this
        return random.random() > 0.5

    def animate_cubic(self, v1, v2, draw_fn, seconds):
        v3 = v2 - v1
        ticks = int(seconds * 30)

        for t in range(ticks):
            draw_fn((v1 + v3 * cubic_distance(t, ticks, ticks) / ticks).xy)
            pygame.display.update()
            self.clock.tick(30)

    def animate_player(self, p, v1, v2, seconds=0.3):
        def draw_fn(xy):
            self.draw_board()
            self.draw_players(ignore_player=p)
            self.screen.blit(
                self.font.render(str(p + 1), True, black),
                xy,
            )

        self.animate_cubic(v1, v2, draw_fn, seconds)

    def animate_move(self, p, n):
        if n > 0:
            positions = [self.players[p] + i for i in range(min(n + 1, 99))]
        else:
            positions = [self.players[p] - i for i in range(min(abs(n + 1), 99))]

        for old, new in zip(positions[:-1], positions[1:]):
            v1 = pygame.math.Vector2(self.squares[old].center)
            v2 = pygame.math.Vector2(self.squares[new].center)
            self.animate_player(p, v1, v2)

    def animate_snake(self, p, head, tail):
        v1 = pygame.math.Vector2(self.squares[head].center)
        v2 = pygame.math.Vector2(self.squares[tail].center)
        self.animate_player(p, v1, v2, seconds=1)

    def animate_ladder(self, p, bottom, top):
        v1 = pygame.math.Vector2(self.squares[bottom].center)
        v2 = pygame.math.Vector2(self.squares[top].center)
        self.animate_player(p, v1, v2, seconds=1)

    def animate_roll(self):
        pass

    def play_turn(self, p, backwards=False):
        # increments current player pos by dice roll
        # TODO: let player hit the roll button
        n = self.roll()
        if backwards:
            n = -n
        self.prompt = f"Player {(self.turn % len(self.players)) + 1} rolled a {n}"
        self.animate_move(p, n)
        self.players[p] += n

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
            minigame_won = self.play_minigame()
            if not minigame_won:
                self.animate_snake(
                    p, self.players[p], self.board.snakes[self.players[p]]
                )
                self.players[p] = self.board.snakes[self.players[p]]
        elif square == sq_ladder:
            minigame_won = self.play_minigame()
            if minigame_won:
                self.animate_ladder(
                    p, self.players[p], self.board.ladders[self.players[p]]
                )
                self.players[p] = self.board.ladders[self.players[p]]
        elif square == sq_special:
            minigame_won = self.play_minigame()
            if minigame_won:
                return self.play_turn(p)
            else:
                return self.play_turn(p, backwards=True)
        else:
            return False

    def draw_board(self):
        self.screen.fill(white)

        pygame.draw.rect(self.screen, blue, self.button_roll)
        self.screen.blit(self.font.render("Roll", True, white), self.button_roll.center)

        self.screen.blit(
            self.font.render(self.prompt, True, black), self.prompt_location
        )

        for i, sq in enumerate(self.squares):
            pygame.draw.rect(self.screen, black, sq, width=3)
            self.screen.blit(self.font.render(str(i + 1), True, black), sq.topleft)

        for start, end in self.board.snakes.items():
            pygame.draw.line(
                self.screen,
                green,
                self.squares[start].center,
                self.squares[end].center,
                width=4,
            )

        for start, end in self.board.ladders.items():
            pygame.draw.line(
                self.screen,
                red,
                self.squares[start].center,
                self.squares[end].center,
                width=4,
            )

        for pos in self.board.special:
            pygame.draw.circle(
                self.screen,
                blue,
                self.squares[pos].center,
                radius=4,
            )

    def draw_players(self, ignore_player=None):
        for p, player in enumerate(self.players):
            if p != ignore_player:
                self.screen.blit(
                    self.font.render(str(p + 1), True, black),
                    self.squares[player].center,
                )

    def play_game(self):
        """Main game loop."""
        self.prompt = f"Player {(self.turn % len(self.players)) + 1}'s turn"
        self.draw_board()
        self.draw_players()
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.button_roll.collidepoint(mouse_pos):
                        if self.play_turn(self.turn % len(self.players)):
                            print(f"p {(self.turn % len(self.players))+1} WON")
                            return
                        self.turn += 1

                        self.prompt += (
                            f", Player {(self.turn % len(self.players)) + 1}'s turn"
                        )
                        self.draw_board()
                        self.draw_players()
                        pygame.display.update()


class Board:
    SNAKE_SQUARE = 0
    LADDER_SQUARE = 1
    SPECIAL_SQUARE = 2

    def __init__(self):
        # {head:tail, bottomladder:topladder, etc}
        # snake heads call minigame
        self.snakes = {96: 77, 94: 55, 87: 23, 61: 17, 47: 25, 35: 5, 31: 9}
        # ladder bottoms call minigame, LADDER MUST NOT GO DIRECTLY TO WIN
        self.ladders = {1: 37, 3: 13, 7: 29, 27: 73, 20: 41, 49: 66, 70: 91, 79: 98}

        # generate 5 random positions for the special squares
        # don't include square 0 or square 99
        used_squares = (
            set(self.snakes.keys())
            | set(self.ladders.keys())
            | set(self.snakes.values())
            | set(self.snakes.keys())
        )
        unused_squares = set(range(1, 99)) - used_squares
        self.special = random.sample(unused_squares, 5)

    def get_coord(self, pos):
        row = pos // 10
        col = pos % 10 if row % 2 == 0 else (9 - pos % 10)
        return row, col

    def get_square(self, pos):
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
    pygame.font.init()
    font = pygame.font.SysFont("timesnewroman", 20)
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
    menu.add.button(
        "Play", lambda: Game(screen, clock, font, w=width, h=height, num_players=2)
    )
    menu.add.button("Help", help_menu)
    menu.add.button("Settings", settings_menu)
    menu.add.button("Quit", pygame_menu.events.EXIT)
    menu.mainloop(screen)
