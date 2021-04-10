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

        self.lad_h = 600
        self.lad_w = 75

        cx, cy = w // 2, h // 2  # center x, center y
        hw, hh = self.lad_w // 2, self.lad_h // 2  # half lad width, half lad height
        self.ladder_rects = [
            pygame.Rect(cx - 5 * hw, cy - hh, self.lad_w, self.lad_h),
            pygame.Rect(cx - 3 * hw, cy - hh, self.lad_w, self.lad_h),
            pygame.Rect(cx - 1 * hw, cy - hh, self.lad_w, self.lad_h),
            pygame.Rect(cx + 1 * hw, cy - hh, self.lad_w, self.lad_h),
            pygame.Rect(cx + 3 * hw, cy - hh, self.lad_w, self.lad_h),
        ]

        # (ladder_num, height)
        # ladder number left to right (0 for leftmost, 2 for rightmost)
        # ladder height (0 for topmost, lad_h - player_h for bottom-most)
        self.player_w = self.lad_w
        self.player_h = int(self.player_w * 1.25)
        self.player = (0, self.lad_h - self.player_h)

    @property
    def player_rect(self):
        lnum = self.player[0]
        lheight = self.player[1]
        return pygame.Rect(
            self.ladder_rects[lnum].left,
            (self.h - self.lad_h) // 2 + lheight,
            self.player_w,
            self.player_h,
        )

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
            pass

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
    pygame.display.set_caption("MINIGAME NAME HERE")
    clock = pygame.time.Clock()

    # start game
    minigame = LadderClimb("easy", screen, clock, font, width, height, fps)
    result = minigame.play_minigame()
    print(f"\n\nGame Result: {result}")
