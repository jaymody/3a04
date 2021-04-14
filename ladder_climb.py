import sys
import time
import random
import pygame
from pygame.locals import RLEACCEL

# constants
rich_black = (26, 27, 41)
white = (255, 255, 255)
orange = (237, 125, 58)
sky_blue = (135, 206, 250)


class Cloud(pygame.sprite.Sprite):
    def __init__(self, w, h, speed, size):
        super().__init__()
        surf = pygame.image.load("assets/ladder_climb/cloud.png").convert_alpha()
        ratio = size / surf.get_height()
        sw, sh = int(ratio*surf.get_width()), int(ratio*surf.get_height())
        self.surf = pygame.transform.scale(surf, (sw, sh))
        self.surf.set_colorkey(sky_blue, RLEACCEL)

        if random.random() < 0.5:
            xpos = random.randint(0, w//4)
        else:
            xpos = random.randint(3*w//4 - sw, w - sw)

        self.rect = self.surf.get_rect(topleft=(xpos, -sh))
        self.h = h
        self.speed = speed

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top >= self.h:
            self.kill()

class FallingSnake(pygame.sprite.Sprite):
    def __init__(self, x, h, speed, size):
        super().__init__()
        self.x = x
        self.h = h
        self.speed = speed
        self.size = size

        surf = pygame.image.load("assets/ladder_climb/falling_snake.png").convert_alpha()
        self.surf = pygame.transform.scale(surf, (size - 2, size))
        self.surf.set_colorkey(sky_blue, RLEACCEL)

        self.rect = self.surf.get_rect(topleft=(x + 1, -size))

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top >= self.h:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size, ladder_positions):
        super().__init__()
        surf = pygame.image.load("assets/ladder_climb/player.png").convert_alpha()
        self.surf = pygame.transform.scale(surf, (size - 2, size))
        self.surf.set_colorkey(sky_blue, RLEACCEL)

        self.pos = 0
        self.ladder_positions = ladder_positions
        self.rect = self.surf.get_rect(topleft=(ladder_positions[self.pos] + 1, y))

    def move_left(self):
        self.pos = max(self.pos - 1, 0)

    def move_right(self):
        self.pos = min(self.pos + 1, len(self.ladder_positions))

    def update(self):
        self.rect.left = self.ladder_positions[self.pos] + 1


class LadderClimb:
    NEW_CLOUD = pygame.USEREVENT + 131
    NEW_SNAKE = pygame.USEREVENT + 132

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
            pygame.Rect(cx - 3 * hw, 0, self.lad_w, self.h),
            pygame.Rect(cx - 1 * hw, 0, self.lad_w, self.h),
            pygame.Rect(cx + 1 * hw, 0, self.lad_w, self.h),
        ]

        self.snakes = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.player = Player(
            self.ladder_rects[0].left,
            self.h - 2 * self.lad_w,
            self.lad_w,
            [rect.left for rect in self.ladder_rects]
        )

        self.elapsed = 0
        if self.difficulty == "easy":
            self.prob = 0.3
            self.speed = int(4 * fps/60)
            self.time_to_beat = 20
        elif self.difficulty == "medium":
            self.prob = 0.35
            self.speed = int(5 * fps/60)
            self.time_to_beat = 25
        elif self.difficulty == "hard":
            self.prob = 0.4
            self.speed = int(6 * fps/60)
            self.time_to_beat = 30

        pygame.time.set_timer(self.NEW_CLOUD, 500)
        pygame.time.set_timer(self.NEW_SNAKE, 50)

        self.new_snake_allowed = True

    def tick_event(self):
        new_allowed = True
        for i, snake in enumerate(self.snakes):
            if snake.rect.colliderect(self.player.rect):
                return True
            if snake.rect.top < 2 * self.lad_w:
                new_allowed = False
        self.new_snake_allowed = new_allowed
        return False

    def handle_event(self, event):
        if event.type == pygame.QUIT or event.type == 32787:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_LEFT:
                self.player.move_left()
            elif key == pygame.K_RIGHT:
                self.player.move_right()
        elif event.type == self.NEW_CLOUD:
            self.clouds.add(Cloud(self.w, self.h, self.speed, self.lad_w))
        elif self.new_snake_allowed and event.type == self.NEW_SNAKE and random.random() < self.prob:
            pos = random.randint(0, len(self.ladder_rects) - 1)
            x = self.ladder_rects[pos].left
            self.snakes.add(FallingSnake(x, self.h, self.speed, self.lad_w))

        return False

    def draw(self):
        # clear screen and draw background
        self.screen.fill(sky_blue)

        # draw ladders
        for rect in self.ladder_rects:
            pygame.draw.rect(self.screen, orange, rect, width=3)

        # draw clouds
        for cloud in self.clouds:
            self.screen.blit(cloud.surf, cloud.rect)

        # draw snakes
        for snake in self.snakes:
            self.screen.blit(snake.surf, snake.rect)

        # draw player
        self.screen.blit(self.player.surf, self.player.rect)


        # textbox description
        pygame.draw.rect(self.screen, rich_black, pygame.Rect(0, 0, 500, 100))

        # draw timer
        self.screen.blit(
            self.font.render("Timer: " + str(int(self.time_to_beat - self.elapsed)), True, white),
            (20, 20),
        )

        # instructions
        self.screen.blit(
            self.font.render("Avoid the snakes", True, white),
            (20, 40),
        )

        self.screen.blit(
            self.font.render("Use the arrows keys to move left and right", True, white),
            (20, 60)
        )

    def play_minigame(self):
        """Return True if minigame is won, else False"""
        self.draw()
        pygame.display.update()
        start = time.time()
        while True:
            if self.tick_event():
                pygame.draw.rect(self.screen, rich_black, pygame.Rect(0, 0, 500, 100))
                self.screen.blit(
                    self.font.render("YOU LOST!", True, white),
                    (20, 40),
                )
                pygame.display.update()
                pygame.time.wait(1500)
                return False

            for event in pygame.event.get():
                self.handle_event(event)

            self.elapsed = time.time() - start
            if self.elapsed > self.time_to_beat:
                pygame.draw.rect(self.screen, rich_black, pygame.Rect(0, 0, 500, 100))
                self.screen.blit(
                    self.font.render("YOU WON!", True, white),
                    (20, 40),
                )
                pygame.display.update()
                pygame.time.wait(1500)
                return True

            self.clouds.update()
            self.snakes.update()
            self.player.update()

            self.clock.tick(self.fps)

            self.draw()
            pygame.display.update()


if __name__ == "__main__":
    # constants
    width = 1280
    height = 720
    fps = 144

    # initialize
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("timesnewroman", 20)
    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption("Ladder Climb")
    clock = pygame.time.Clock()

    # start game
    minigame = LadderClimb("hard", screen, clock, font, width, height, fps)
    result = minigame.play_minigame()
    print(f"\n\nGame Result: {result}")
