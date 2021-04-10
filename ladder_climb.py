import sys
import pygame

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)


class LadderClimb:
    def __init__(self, difficulty, screen, clock, font, w, h, fps):
        self.difficulty = difficulty
        self.screen = screen
        self.clock = clock
        self.font = font
        self.w, self.h = w, h
        self.fps = fps

        self.lad_w = 75

        cx, hw = self.w // 2, self.lad_w // 2  # center x, half ladder width
        self.ladder_rects = [
            pygame.Rect(cx - 5 * hw, 0, self.lad_w, self.h),
            pygame.Rect(cx - 3 * hw, 0, self.lad_w, self.h),
            pygame.Rect(cx - 1 * hw, 0, self.lad_w, self.h),
            pygame.Rect(cx + 1 * hw, 0, self.lad_w, self.h),
            pygame.Rect(cx + 3 * hw, 0, self.lad_w, self.h),
        ]

        self.player_w = self.lad_w
        self.player_h = int(self.player_w * 1.25)
        self.ladder = 0  # the ladder the player is on

    @property
    def player_rect(self):
        return pygame.Rect(
            self.ladder_rects[self.ladder].left,
            self.h - 2 * self.player_h,
            self.player_w,
            self.player_h,
        )

    def handle_event(self, event):
        if event.type == pygame.QUIT or event.type == 32787:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_LEFT:
                self.ladder = max(self.ladder - 1, 0)
            elif key == pygame.K_RIGHT:
                self.ladder = min(self.ladder + 1, len(self.ladder_rects) - 1)

    def draw(self):
        # clear screen and draw background
        self.screen.fill(white)

        # draw ladders
        for rect in self.ladder_rects:
            pygame.draw.rect(self.screen, black, rect, width=3)

        # draw player
        pygame.draw.rect(self.screen, blue, self.player_rect)

    def play_minigame(self):
        """Return True if minigame is won, else False"""
        self.draw()
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                self.handle_event(event)

            self.clock.tick(self.fps)

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
    pygame.display.set_caption("Ladder Climb")
    clock = pygame.time.Clock()

    # start game
    minigame = LadderClimb("easy", screen, clock, font, width, height, fps)
    result = minigame.play_minigame()
    print(f"\n\nGame Result: {result}")
