import pygame

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)


class DummyMinigame:
    def __init__(self, difficulty, screen, clock, font, w, h, fps):
        self.difficulty = difficulty
        self.screen = screen
        self.clock = clock
        self.font = font
        self.w, self.h = w, h
        self.fps = fps

    def draw(self):
        # clear screen and draw background
        self.screen.fill(white)

        # draw some text
        self.screen.blit(
            self.font.render(f"difficulty = {self.difficulty}", True, black),
            (200, 200),
        )
        import time

        self.screen.blit(
            self.font.render(f"time = {time.time()}", True, black),
            (300, 300),
        )

        # draw a square
        pygame.draw.rect(self.screen, black, pygame.Rect(100, 100, 20, 20))

    def play_minigame(self):
        """Return True if minigame is won, else False"""
        self.draw()
        pygame.display.update()
        while True:
            ###### DELETE THE BELOW AND ADD GAME LOGIC ######
            import time
            import random

            if random.random() < 1 / (10 * self.fps):
                return random.random() < 0.5

            self.clock.tick(self.fps)
            ###### DELETE THE BELOW AND ADD GAME LOGIC ######

            self.draw()
            pygame.display.update()


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
    pygame.display.set_caption("MINIGAME NAME HERE")
    clock = pygame.time.Clock()

    # start game
    minigame = DummyMinigame("easy", screen, clock, font, width, height, fps)
    result = minigame.play_minigame()
    print(f"\n\nGame Result: {result}")
