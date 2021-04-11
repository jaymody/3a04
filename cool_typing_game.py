from pygame.locals import *
import pygame
import sys
import random

# constants
TOTAL_TIME = 15
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (255, 240, 219)
WORD_BACKGROUND = (26, 27, 41)
GREEN = (36, 201, 94)
YELLOW = (245, 235, 47)
RED = (255, 59, 59)

def draw_text(text, font, color, screen, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    screen.blit(textobj, textrect)

class Difficulty:

    def __init__(self, diff):
        self.diff = diff

    def diff_len(self):
        if (self.diff == "easy"):
            return lambda word: len(word) < 6
        elif (self.diff == "medium"):
            return lambda word: len(word) < 9
        return lambda word: len(word) > 6

    def diff_time(self):
        return 0.5

    def diff_win_cond(self):
        return 5

# TODO
# integrate with game.py
# UI
# Actual snake charming game

class TypingGame:

    spawn_word_event = pygame.USEREVENT + 1
    spawn_delay = 150
    clear_prev_word_event = pygame.USEREVENT + 2
    clear_delay = 750

    snake = pygame.image.load('./assets/snake.png')

    def __init__(self, diff, screen, clock, font, width, height, fps):

        pygame.mixer.init()
        self.correct_word = pygame.mixer.Sound("./assets/correct.mp3")
        self.incorrect_word = pygame.mixer.Sound("./assets/incorrect.mp3")
        self.bgm = pygame.mixer.Sound("./assets/not_kahoot.mp3")

        pygame.key.set_repeat(400, 35)

        self.diff = Difficulty(diff)
        self.screen = screen
        self.clock = clock
        self.font = font
        self.width = width
        self.height = height
        self.fps = fps
        
        self.words = self.read_words()
        self.typed_word = "Start Typing..."
        self.game_over = False
        self.win = False
        self.start_game = False
        self.spawned_words = [("", 0, BACKGROUND), ("", 0, BACKGROUND), ("", 0, BACKGROUND), ("", 0, BACKGROUND)]
        self.prev_word = ""
        self.correct_words = 0
        self.prev_word_index = -1
        self.foo = True

        self.play_minigame()

    def read_words(self):
        words = []
        with open("./assets/words.txt", "r") as reader:
            line = reader.readline()
            while line != "":
                words.append(line[:len(line)-1])
                line = reader.readline()
        return words

    def free_index(self):
        for i, word in enumerate(self.spawned_words):
            if (word[0] == "" and i != self.prev_word_index):
                return i
        return -1

    def spawn_word(self):
        filtered_words = list(filter(self.diff.diff_len(), self.words))
        while True:
            idx = random.randint(0, len(filtered_words) - 1)
            valid_word = True
            # if the random word is already spawned
            for word in self.spawned_words:
                if (filtered_words[idx] == word[0]):
                    valid_word = False
                    break
            # if the random word has spawned recently
            if (filtered_words[idx] == self.prev_word):
                valid_word = False
            if (valid_word): 
                break

        return filtered_words[idx]
    
    def despawn_word(self, curr_time):
        for i, word in enumerate(self.spawned_words):
            if (curr_time - word[1] > self.diff.diff_time() * len(word[0])):
                self.spawned_words[i] = ("", word[1], BACKGROUND)

    def get_colour(self, len, spawn_time):
        diff_time = self.diff.diff_time() * len
        if (spawn_time < diff_time / 3):
            return GREEN
        elif (spawn_time < diff_time / 3 * 2):
            return YELLOW
        return RED

    # could probably math it out instead of hard coding
    def calc_word_pos(self, index):
        if (index == 0):
            return (self.width/5*2, self.height/3*2)
        elif (index == 1):
            return (self.width/5*3, self.height/3*2)
        elif (index == 2):
            return (self.width/5*2, self.height/7*6)
        return (self.width/5*3, self.height/7*6)

    def draw_snake(self):
        # drawing snake itself
        snake_rect = self.snake.get_rect()
        snake_rect.center = (self.width/2, self.height/4)
        self.screen.blit(self.snake, snake_rect)
        # draw snake hp
        hp = pygame.Rect(self.width/2, self.height/5, 240, 25)
        hp.center = (self.width/2, self.height/18)
        pygame.draw.rect(self.screen, RED, hp)
    
    def user_submit(self):
        correct = False
        for i, word in enumerate(self.spawned_words):
            if (self.typed_word.lower() == word[0].lower() and self.typed_word != ""):
                correct = True
                self.spawned_words[i] = ("", -9999, BACKGROUND)
                self.prev_word_index = i
                pygame.time.set_timer(self.clear_prev_word_event, self.clear_delay, True)
                self.prev_word = word[0]
                break
        if (correct):
            self.correct_words += 1
            pygame.mixer.Sound.play(self.correct_word)
            pygame.mixer.music.stop()
        else:
            pygame.mixer.Sound.play(self.incorrect_word)
            pygame.mixer.music.stop()
        self.typed_word = ""
       
    def play_minigame(self):

        while True:
            
            # start game loop
            while not self.start_game:
                self.clock.tick(self.fps)
                self.screen.fill(BACKGROUND)
                draw_text("PRESS ANY BUTTON TO START GAME", font, BLACK, self.screen, self.width/2, self.height/2)
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        self.start_game = True
                    elif event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.update()


            # main game loop
            pygame.time.set_timer(self.spawn_word_event, self.spawn_delay)
            pygame.mixer.Sound.play(self.bgm)

            start_tick = pygame.time.get_ticks() / 1000
            end_tick = pygame.time.get_ticks() / 1000

            while not self.game_over:

                self.clock.tick(self.fps)
                self.screen.fill(BACKGROUND)
                elapsed_time = end_tick - start_tick
                draw_text("Time Leftc:", font, BLACK, self.screen, self.width/12, self.height/15)
                draw_text(str(round(TOTAL_TIME - elapsed_time, 3)), font, BLACK, self.screen, self.width/6, self.height/15)
                end_tick = pygame.time.get_ticks() / 1000

                if (elapsed_time > TOTAL_TIME):
                    self.game_over = True

                # draw boss snake
                self.draw_snake()

                # draw word backgrounds
                for i in range(len(self.spawned_words)):
                    bg = pygame.Rect(self.width, self.height, 240, 120)
                    bg.center = self.calc_word_pos(i)
                    pygame.draw.rect(self.screen, WORD_BACKGROUND, bg)

                # draws all words
                for i, word in enumerate(self.spawned_words):
                    self.spawned_words[i] = (word[0], word[1], self.get_colour(len(word[0]), elapsed_time - word[1]))
                    word_pos = self.calc_word_pos(i)
                    draw_text(word[0], font, word[2], self.screen, word_pos[0], word_pos[1])

                # despawns any expired words
                self.despawn_word(elapsed_time)

                if (self.correct_words > self.diff.diff_win_cond()):
                    break

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == self.spawn_word_event:
                        index = self.free_index()
                        if (index != -1):
                            self.spawned_words[index] = ((self.spawn_word(), elapsed_time, GREEN))
                    elif event.type == self.clear_prev_word_event:
                        self.prev_word_index = -1
                    elif event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            self.user_submit()
                        elif event.key == K_BACKSPACE:
                            self.typed_word = self.typed_word[:-1]
                        elif event.key == K_ESCAPE:
                            self.typed_word = ""
                        else:
                            if (self.typed_word == "Start Typing..."):
                                self.typed_word = ""
                            self.typed_word += event.unicode
                pygame.event.clear()

                typed_bg = pygame.Rect(self.width, self.height, 250, 60)
                typed_bg.center = (self.width/2, self.height/2)
                pygame.draw.rect(self.screen, WORD_BACKGROUND, typed_bg)
                draw_text(self.typed_word, font, WHITE, self.screen, self.width/2, self.height/2)

                pygame.display.update()

            pygame.event.clear()
            pygame.mixer.pause()
            # end game loop
            while True:
                self.clock.tick(self.fps)
                self.screen.fill(BACKGROUND) 
                if (self.correct_words > self.diff.diff_win_cond()):
                    self.win = True
                draw_text("YOU WIN" if self.win else "YOU LOSE", font, BLACK, self.screen, self.width/2, self.height/2)
                draw_text("PRESS ANY BUTTON TO GO BACK TO GAME", font, BLACK, self.screen, self.width/2, self.height*2/3)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        return self.win
                pygame.display.update()

if __name__ == "__main__":
    # constants
    width = 1280
    height = 720
    fps = 60
    diff = "easy" # easy, medium or hard

    # initialize
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("comicsansms", 20)
    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption('Snake Charmer 9000')
    clock = pygame.time.Clock()

    # start game
    minigame = TypingGame(diff, screen, clock, font, width, height, fps)
    result = minigame.play_minigame()
    print(f"\n\nGame Result: {result}")
