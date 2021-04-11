#Imports n stuff
import sys
import pygame
import time
import random


class SnakeGame:
    def __init__(self, difficulty, screen, clock, font, w, h, fps):
        self.difficulty = difficulty
        self.screen = screen
        self.clock = clock
        self.font = font
        self.w = w
        self.h = h
        self.fps = fps

        #Snake head size
        self.snake_block = 40

        #Different speeds for different difficulties
        if difficulty == 'easy':
            self.snake_speed = 15
        elif difficulty == 'medium':
            self.snake_speed = 18
        else:
            self.snake_speed = 21

    #Displays amount of food needed to win the game
    def Your_score(self, score):
        value = score_font.render("Food needed to win: " + str(score), True, font_green)
        dis.blit(value, [0, 0])



    def our_snake(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis, snake_green, [x[0], x[1], snake_block, snake_block])

    def message(self, msg, color):
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [self.w / 2, self.h / 3])


    def play_minigame(self):
        game_over = False
        game_close = False

        x1 = self.w / 2
        y1 = self.h / 2

        x1_change = 0
        y1_change = 0

        if self.difficulty == 'easy':
            food_to_win = 8
        elif self.difficulty == 'medium':
            food_to_win = 7
        else:
            food_to_win = 6
        
        curr_dir = 5
        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, self.w - self.snake_block)/40.0) * 40.0
        foody = round(random.randrange(0, self.h - self.snake_block)/40.0) * 40.0

        dis.fill(bg_green)
        self.Your_score(food_to_win)
        self.message("Use the arrow keys to move and collect food!", font_green)
        while not game_over:
            
            if food_to_win == 0:
                dis.fill(bg_green)
                self.message("You win!", white)
                self.Your_score(food_to_win)
                pygame.display.update()
                pygame.time.wait(1500)
                return True

            while game_close == True:
                dis.fill(bg_green)
                self.message("You Lost!", red)
                self.Your_score(food_to_win)
                pygame.display.update()
                pygame.time.wait(1500)
                return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and curr_dir != 1:
                        x1_change = -self.snake_block
                        y1_change = 0
                        curr_dir = 3
                    elif event.key == pygame.K_RIGHT and curr_dir != 3:
                        x1_change = self.snake_block
                        y1_change = 0
                        curr_dir = 1
                    elif event.key == pygame.K_UP and curr_dir != 2:
                        y1_change = -self.snake_block
                        x1_change = 0
                        curr_dir = 0
                    elif event.key == pygame.K_DOWN and curr_dir != 0:
                        y1_change = self.snake_block
                        x1_change = 0
                        curr_dir = 2

            if x1 >= self.w or x1 < 0 or y1 >= self.h or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change
            dis.fill(bg_green)
            pygame.draw.rect(dis, green, [foodx, foody, self.snake_block, self.snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            self.our_snake(self.snake_block, snake_List)
            self.Your_score(food_to_win)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, self.w - self.snake_block) / 40.0) * 40.0
                foody = round(random.randrange(0, self.h - self.snake_block) / 40.0) * 40.0
                if self.difficulty == 'easy':
                    Length_of_snake += 2
                elif self.difficulty == 'medium':
                    Length_of_snake += 3
                else:
                    Length_of_snake += 5
                food_to_win -= 1

            clock.tick(self.snake_speed)
        return True

#Colour constants
snake_green = (0, 51, 0)
white = (255, 255, 255)
font_green = (51, 90, 45)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
bg_green = (90, 138, 83)

dis = pygame.display.set_mode((1280, 720))

 
clock = pygame.time.Clock()
 
if __name__ == "__main__":
    # constants
    width = 1280
    height = 720
    fps = 60

    # initialize
    pygame.init()
    pygame.font.init()
    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)

    pygame.display.set_caption('Snake Game')

    screen = pygame.display.set_mode([width, height])
    clock = pygame.time.Clock()

    # start game
    minigame = SnakeGame("easy", screen, clock, font_style, width, height, fps)
    result = minigame.play_minigame()
    print(f"\n\nGame Result: {result}")