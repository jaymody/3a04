import pygame
import sys
import os
import time
import random


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
pink = (150, 0, 150)


class Button:
    def __init__(self, screen, font, color, x, y, width, height, text=""):
        self.screen = screen
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(
                self.screen,
                outline,
                (self.x - 2, self.y - 2, self.width + 4, self.height + 4),
                0,
            )

        pygame.draw.rect(
            self.screen, self.color, (self.x, self.y, self.width, self.height), 0
        )

        if self.text != "":

            text = self.font.render(self.text, 1, (0, 0, 0))
            self.screen.blit(
                text,
                (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y + (self.height / 2 - text.get_height() / 2),
                ),
            )

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class SimonSays:
    def __init__(self, difficulty, screen, clock, font, w, h, fps):
        self.difficulty = difficulty
        self.screen = screen
        self.clock = clock
        self.font = font
        self.w, self.h = w, h
        self.fps = fps

        background_image = pygame.image.load(os.path.join("images", "BACKGROUND.jpeg"))
        self.backgroundResize = pygame.transform.scale(background_image, (850, 550))

        game_image = pygame.image.load(os.path.join("images", "GAMEBACK.jpeg"))
        self.gameImageResize = pygame.transform.scale(game_image, (850, 550))

        self.font = pygame.font.SysFont("comicsans", 25)

        if self.difficulty == "easy":
            grid_size = 3
            self.num_squares_to_click = 3
            self.time_to_see_square = 1000  # in ms

        if self.difficulty == "medium":
            grid_size = 4
            self.num_squares_to_click = 4
            self.time_to_see_square = 1000  # in ms

        if self.difficulty == "hard":
            grid_size = 5
            self.num_squares_to_click = 5
            self.time_to_see_square = 1000  # in ms

        size = 100
        startx, starty = 40, 40
        gap = 10

        xywh = []
        for i in range(grid_size):
            for j in range(grid_size):
                x = startx + i * size + i * gap
                y = starty + j * size + j * gap
                xywh.append([x, y, size, size])

        self.rects = []
        for x, y, w, h in xywh:
            self.rects.append(pygame.Rect(x, y, w, h))

    def draw_startwindow(self):
        self.screen.fill(white)

        self.screen.blit(self.backgroundResize, (1, 1))
        # x,y,width,height
        pygame.draw.rect(self.screen, (0, 0, 0), (58, 78, 650, 62))
        pygame.draw.rect(self.screen, (255, 255, 255), (60, 80, 640, 56))

        # The text
        instructionsText1 = self.font.render(
            "Welcome to Simon Says! You have to click the buttons in the ",
            True,
            (0, 0, 0),
        )
        instructionsText2 = self.font.render(
            "order they appear on the screen! Are you ready?", True, (0, 0, 0)
        )

        self.screen.blit(instructionsText1, (80, 90))

        self.screen.blit(instructionsText2, (80, 115))

    def minigame(self):
        # background
        self.screen.fill(white)
        self.screen.blit(self.gameImageResize, (0, 0))

        # draw rectangles
        for rect in self.rects:
            pygame.draw.rect(self.screen, pink, rect)

        # show tiles
        pygame.display.update()
        pygame.time.wait(3000)
        
        # grey out 3 tiles
        grey_rects = random.sample(self.rects, self.num_squares_to_click)
        for rect in grey_rects:
            # draw grey rect
            pygame.draw.rect(self.screen, black, rect)
            pygame.display.update()
            pygame.time.wait(self.time_to_see_square)

            # undraw grey rect
            pygame.draw.rect(self.screen, pink, rect)
            pygame.display.update()

        cur_square = 0
        while True:
            # exit the game if the user wants
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # if user clicks on button to start game
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect in self.rects:
                        if rect.collidepoint(pos):
                            if rect == grey_rects[cur_square]:
                                cur_square += 1
                                pygame.draw.rect(self.screen, blue, rect)
                                pygame.display.update()
                                pygame.time.wait(200)
                                pygame.draw.rect(self.screen, pink, rect)
                                pygame.display.update()
                                if cur_square >= len(grey_rects):
                                    return True
                            else:
                                pygame.draw.rect(self.screen, red, rect)
                                pygame.display.update()
                                pygame.time.wait(500)
                                return False
            self.clock.tick(self.fps)

    def play_minigame(self):
        """Return True if minigame is won, else False"""
        startwindow = True

        # draw start window
        self.draw_startwindow()
        playbutton = Button(
            self.screen,
            self.font,
            (
                0,
                200,
                220,
            ),
            150,
            225,
            250,
            100,
            "Play game",
        )
        playbutton.draw((0, 0, 0))
        pygame.display.update()

        while True:
            # exit the game if the user wants
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # if user clicks on button to start game
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playbutton.isOver(pos):
                        return self.minigame()

            self.clock.tick(self.fps)


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
    pygame.display.set_caption("Simon Says")
    clock = pygame.time.Clock()

    # start game
    minigame = SimonSays("hard", screen, clock, font, width, height, fps)
    result = minigame.play_minigame()
    print(f"\n\nGame Result: {result}")
