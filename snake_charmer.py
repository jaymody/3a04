from pygame import draw
from pygame.locals import *
import pygame
import sys
import random

# constants
RICH_BLACK = (26, 27, 41)
AZURE = (230, 250, 252)
EMERALD = (47, 191, 113)
PRINCETON_ORANGE = (237, 125, 58)
ORANGE = (247, 149, 27)
RED = (239, 45, 86)

def draw_text(text, font, color, screen, x, y, center=True):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
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

    def word_multi(self):
        return 0.5

    def damage_multi(self):
        if (self.diff == "easy"):
            return 30
        elif (self.diff == "medium"):
            return 25
        return 20
    
    def total_time(self):
        if (self.diff == "easy"):
            return 15
        elif (self.diff == "medium"):
            return 18
        return 20

    def snake_hp(self):
        if (self.diff == "easy"):
            return 1000
        elif (self.diff == "medium"):
            return 1200
        return 1400

class Snake(pygame.sprite.Sprite):

    def __init__(self, screen, width, height, font, max_hp):

        super().__init__()
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.image = pygame.image.load('./assets/snake_charm/snake.png')
        self.rect = self.image.get_rect(center = (width/2, height/4))
        self.current_health = self.maximum_health = self.target_health = max_hp
        self.health_bar_length = 400
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_change_speed = 5
    
    def update(self):
        self.health_bar()
    
    def health_bar(self):
        transition_width = 0
        transition_colour = RED

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = (self.current_health - self.target_health) // self.health_ratio
            transition_colour = PRINCETON_ORANGE

        hp_rect  = pygame.Rect((self.width - self.health_bar_length)/2, self.height/20, self.current_health / self.health_ratio, 25)
        transition_bar_rect  = pygame.Rect(hp_rect.right - transition_width, self.height/20, transition_width, 25)

        pygame.draw.rect(self.screen, RED, hp_rect)
        pygame.draw.rect(self.screen, transition_colour, transition_bar_rect)
        pygame.draw.rect(self.screen, AZURE, ((self.width - self.health_bar_length)/2, self.height/20, self.health_bar_length, 25), 3)
        draw_text("HP: " + str(self.current_health), self.font, AZURE, self.screen, self.width/2, transition_bar_rect.centery)

    def change_snake(self, win):
        if win:
            self.image = pygame.image.load('./assets/snake_charm/happy_snake.png')
        else:
            self.image = pygame.image.load('./assets/snake_charm/mad_snake.png')

    def get_visual_hp(self):
        return self.current_health

    def get_actual_hp(self):
        return self.target_health

    def hit_snake(self, damage):
        if self.target_health > 0:
            self.target_health -= damage
        if self.target_health < 0:
            self.target_health = 0

# TODO
# UI
# snake movement

class SnakeCharmer:

    spawn_word_event = pygame.USEREVENT + 1
    spawn_delay = 250
    clear_prev_word_event = pygame.USEREVENT + 2
    clear_delay = 750

    def __init__(self, diff, screen, clock, font, width, height, fps):

        pygame.mixer.init()
        self.correct_word = pygame.mixer.Sound("./assets/snake_charm/correct.mp3")
        self.incorrect_word = pygame.mixer.Sound("./assets/snake_charm/incorrect.mp3")
        self.type = pygame.mixer.Sound("./assets/snake_charm/type.wav")
        self.type.set_volume(0.4)

        self.instructions_img = pygame.image.load('./assets/snake_charm/instructions.png')

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
        self.total_time = self.diff.total_time()
        self.game_over = False
        self.win = False
        self.start_game = False
        self.spawned_words = [("", 0, RICH_BLACK), ("", 0, RICH_BLACK), ("", 0, RICH_BLACK), ("", 0, RICH_BLACK)]
        self.prev_words = []
        self.prev_word_index = -1
        self.snake = pygame.sprite.GroupSingle(Snake(screen, width, height, font, self.diff.snake_hp()))

        self.play_minigame()

    def read_words(self):
        words = []
        with open("./assets/snake_charm/words.txt", "r") as reader:
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
            if (filtered_words[idx] in self.prev_words):
                valid_word = False
            if (valid_word): 
                break

        return filtered_words[idx]
    
    def prev_words_queue(self, word):
        if (word == ""): return
        if len(self.prev_words) == 4:
            self.prev_words.pop(0)
        self.prev_words.append(word)
    
    def despawn_word(self, curr_time):
        for i, word in enumerate(self.spawned_words):
            if (curr_time - word[1] > self.diff.word_multi() * len(word[0])):
                self.prev_words_queue(word[0])
                self.spawned_words[i] = ("", word[1], RICH_BLACK)

    def get_colour(self, len, spawn_time):
        diff_time = self.diff.word_multi() * len
        if (spawn_time < diff_time / 3):
            return EMERALD
        elif (spawn_time < diff_time / 3 * 2):
            return PRINCETON_ORANGE
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
        self.snake.draw(self.screen)
        self.snake.update()

    def instructions(self):

        running = True
        click = False

        self.spawned_words = [(self.spawn_word(), 0, EMERALD), (self.spawn_word(), 0, PRINCETON_ORANGE), (self.spawn_word(), 0, RED), (self.spawn_word(), 0, EMERALD)]
        while running:
            self.clock.tick(self.fps)
    
            self.screen.fill(RICH_BLACK)
           
            self.screen.blit(self.instructions_img, (0, 0))

            mx, my = pygame.mouse.get_pos()

            back_button = pygame.Rect(50, 100, 100, 40)
            back_button.center = (self.width/18, self.height/7*6)

            if back_button.collidepoint((mx, my)):
                if click:
                    running = False
                    break

            click = False

            pygame.draw.rect(self.screen, AZURE, back_button, 0, 100)
            draw_text('Back', self.font, RICH_BLACK, self.screen, self.width/18, self.height/7*6)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            
            pygame.display.update()

    def menu(self):

        click = False
        
        while not self.start_game:

            self.clock.tick(self.fps)
            self.screen.fill(RICH_BLACK)
            draw_text("Welcome to Snake Charmer!", self.font, AZURE, self.screen, self.width/2, self.height/4)
            mx, my = pygame.mouse.get_pos()
    
            play_button = pygame.Rect(50, 100, 200, 50)
            instruction_button = pygame.Rect(50, 200, 200, 50)
            play_button.center = (self.width/2, self.height/2 - 50)
            instruction_button.center = (self.width/2, self.height/2 + 50)

            if play_button.collidepoint((mx, my)):
                if click:
                    self.start_game = True
                    break
            if instruction_button.collidepoint((mx, my)):
                if click:
                    self.instructions()

            pygame.draw.rect(self.screen, AZURE, play_button, 0, 100)
            draw_text('Play Game', self.font, RICH_BLACK, self.screen, self.width/2, self.height/2 - 50)
            pygame.draw.rect(self.screen, AZURE, instruction_button, 0, 100)
            draw_text('Instructions', self.font, RICH_BLACK, self.screen, self.width/2, self.height/2 + 50)
    
            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
    
            pygame.display.update()

    def user_submit(self):
        correct = False
        for i, word in enumerate(self.spawned_words):
            if (self.typed_word.lower() == word[0].lower() and self.typed_word != ""):
                correct = True
                self.spawned_words[i] = ("", -9999, RICH_BLACK)
                self.prev_word_index = i
                pygame.time.set_timer(self.clear_prev_word_event, self.clear_delay, True)
                self.prev_words_queue(word[0])
                break
        if (correct):
            damage = len(self.typed_word) * self.diff.damage_multi()
            self.snake.sprite.hit_snake(damage)
            pygame.mixer.Sound.play(self.correct_word)
            pygame.mixer.music.stop()
        else:
            pygame.mixer.Sound.play(self.incorrect_word)
            pygame.mixer.music.stop()
        self.typed_word = ""
       
    def play_minigame(self):

        while True:
            
            # start game loop
            self.menu()

            # main game loop
            self.spawned_words = [("", 0, RICH_BLACK), ("", 0, RICH_BLACK), ("", 0, RICH_BLACK), ("", 0, RICH_BLACK)]

            pygame.time.set_timer(self.spawn_word_event, self.spawn_delay)

            start_tick = pygame.time.get_ticks() / 1000
            end_tick = pygame.time.get_ticks() / 1000

            while not self.game_over:

                self.clock.tick(self.fps)
                self.screen.fill(RICH_BLACK)
                elapsed_time = end_tick - start_tick
                draw_text("Time Left: " + str(round(self.total_time - elapsed_time, 3)), self.font, AZURE, self.screen, self.width/12, self.height/20, False)
                end_tick = pygame.time.get_ticks() / 1000

                # check to see if the game is lost
                if (elapsed_time > self.total_time):
                    self.game_over = True
                    break

                # draw boss snake
                self.draw_snake()

                # draw word backgrounds
                for i in range(len(self.spawned_words)):
                    bg = pygame.Rect(self.width, self.height, 240, 120)
                    bg.center = self.calc_word_pos(i)
                    pygame.draw.rect(self.screen, AZURE, bg, 4, 15)

                # draws all words
                for i, word in enumerate(self.spawned_words):
                    self.spawned_words[i] = (word[0], word[1], self.get_colour(len(word[0]), elapsed_time - word[1]))
                    word_pos = self.calc_word_pos(i)
                    if (word[0] != ""):
                        draw_text(word[0], self.font, word[2], self.screen, word_pos[0], word_pos[1] - 20)
                        draw_text(str(len(word[0]) * self.diff.damage_multi()), self.font, AZURE, self.screen, word_pos[0], word_pos[1] + 20)

                 # draws background of where user types
                typed_bg = pygame.Rect(self.width, self.height, 250, 45)
                typed_bg.center = (self.width/2, self.height/2)
                pygame.draw.rect(self.screen, AZURE, typed_bg, 0, 15)
                # draws users text
                draw_text(self.typed_word, self.font, RICH_BLACK, self.screen, self.width/2, self.height/2)

                # despawns any expired words
                self.despawn_word(elapsed_time)

                # check to see if game is won
                if self.snake.sprite.get_visual_hp() <= 0:
                    self.game_over = True
                    break

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == self.spawn_word_event:
                        index = self.free_index()
                        if (index != -1):
                            self.spawned_words[index] = ((self.spawn_word(), elapsed_time, EMERALD))
                    elif event.type == self.clear_prev_word_event:
                        self.prev_word_index = -1
                    elif event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            self.user_submit()
                        elif event.key == K_BACKSPACE:
                            pygame.mixer.Sound.play(self.type)
                            pygame.mixer.music.stop()
                            self.typed_word = self.typed_word[:-1]
                        elif event.key == K_ESCAPE:
                            self.typed_word = ""
                        else:
                            pygame.mixer.Sound.play(self.type)
                            pygame.mixer.music.stop()
                            if (self.typed_word == "Start Typing..."):
                                self.typed_word = ""
                            self.typed_word += event.unicode

                pygame.display.update()

            # end game loop
            while True:
                if self.snake.sprite.get_actual_hp() <= 0:
                    self.win = True
                self.screen.fill(RICH_BLACK)
                self.snake.sprite.change_snake(self.win)
                self.snake.draw(self.screen)
                draw_text("You win!" if self.win else "You lose!", self.font, AZURE, self.screen, self.width/2, self.height/2 - 10)
                pygame.display.update()
                pygame.time.wait(1000)
                return self.win
                

if __name__ == "__main__":
    # constants
    width = 1280
    height = 720
    fps = 60
    diff = "hard" # easy, medium or hard

    # initialize
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("timesnewroman", 20)
    screen = pygame.display.set_mode([width, height])
    pygame.display.set_caption('Snake Charmer 9000')
    clock = pygame.time.Clock()

    # start game
    minigame = SnakeCharmer(diff, screen, clock, font, width, height, fps)
    result = minigame.play_minigame()
    print(f"\n\nGame Result: {result}")
