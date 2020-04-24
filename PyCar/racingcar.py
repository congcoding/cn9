import pygame
import random
from time import sleep

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))


WINDOW_WIDTH = 480
WINDOW_HEIGHT = 600

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)

class Car:
    image_car = ['./PyCar/RacingCar01.png', './PyCar/RacingCar02.png', './PyCar/RacingCar03.png', './PyCar/RacingCar04.png', './PyCar/RacingCar05.png', \
                 './PyCar/RacingCar06.png', './PyCar/RacingCar07.png', './PyCar/RacingCar08.png', './PyCar/RacingCar09.png', './PyCar/RacingCar10.png', \
                 './PyCar/RacingCar11.png', './PyCar/RacingCar12.png', './PyCar/RacingCar13.png', './PyCar/RacingCar14.png', './PyCar/RacingCar15.png', \
                 './PyCar/RacingCar16.png', './PyCar/RacingCar17.png', './PyCar/RacingCar18.png', './PyCar/RacingCar19.png', './PyCar/RacingCar20.png', ]

    def __init__(self, x=0, y=0, dx=0, dy=0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def load_image(self):
        self.image = pygame.image.load(random.choice(self.image_car))
        self.width = self.image.get_rect().size[0]
        self.height = self.image.get_rect().size[1]

    def draw_image(self):
        screen.blit(self.image, [self.x, self.y])

    def move_x(self):
        self.x += self.dx

    def move_y(self):
        self.y += self.dy

    def check_out_of_screen(self):
        if self.x+self.width > WINDOW_WIDTH or self.x < 0:
            self.x -= self.dx

    def check_crash(self, car):
        if (self.x+self.width > car.x) and (self.x < car.x+car.width) and (self.y < car.y+car.height) and (self.y+self.height > car.y):
            return True
        else:
            return False

def draw_main_menu(score):
    draw_x = (WINDOW_WIDTH / 2) - 200
    draw_y = WINDOW_HEIGHT / 2
    image_intro = pygame.image.load('./PyCar/PyCar.png')
    screen.blit(image_intro, [draw_x, draw_y - 280])
    font_40 = pygame.font.SysFont("FixedSys", 40, True, False)
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    text_title = font_40.render("PyCar: Racing Car Game", True, BLACK)
    screen.blit(text_title, [draw_x, draw_y])
    score_text = font_40.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, [draw_x, draw_y + 70])
    text_start = font_30.render("Press Space Key to Start!", True, RED)
    pygame.display.flip()

def draw_score(score):
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    txt_score = font_30.render("Score: " + str(score), True, BLACK)
    screen.blit(txt_score, [15, 15])  

def main_loop():
    pygame.init()

    pygame.display.set_caption("PyCar: Racing Car Game")
    clock = pygame.time.Clock()

    #게임 사운드
    pygame.mixer.music.load('./PyCar/race.wav')
    sound_crash = pygame.mixer.Sound('./PyCar/crash.wav')
    sound_engine = pygame.mixer.Sound('./PyCar/engine.wav')

    #사용자 레이싱 카 생성
    player = Car(WINDOW_WIDTH / 2, (WINDOW_HEIGHT - 150), 0, 0)
    player.load_image()

    #컴퓨터 레이싱 카 생성
    cars = []
    score = 0
    car_count = 3
    for i in range(car_count):
        x = random.randrange(0, WINDOW_WIDTH - 55)
        car = Car(x, random.randrange(-150, -50), 0, random.randint(5, 10))
        car.load_image()
        cars.append(car)
    
    #도로 차선 생성
    lanes = []
    lane_width = 10
    lane_height = 80
    lane_margin = 20
    lane_count = 10
    lane_x = (WINDOW_WIDTH - lane_width) / 2
    lane_y = -10
    for i in range(lane_count):
        lanes.append([lane_x, lane_y])
        lane_y += lane_height + lane_margin

    crash = True
    game_on = True
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                
            if crash:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                    import Start
                    Start.main_loop()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    crash = False
                    for i in range(car_count):
                        cars[i].x = random.randrange(0, WINDOW_WIDTH - cars[i].width)
                        cars[i].y = random.randrange(-150, -50)
                        cars[i].load_image()

                    player.load_image()
                    player.x = 175
                    player.dx = 0
                    score = 0
                    pygame.mouse.set_visible(False)
                    sound_engine.play()
                    sleep(5)
                    pygame.mixer.music.play(-1)

            if not crash:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.dx = 4
                    elif event.key == pygame.K_LEFT:
                        player.dx = -4

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.dx = 0
                    elif event.key == pygame.K_RIGHT:
                        player.dx = 0

        #GRAY로 화면 채우기
        screen.fill(GRAY)

        #게임 화면 출력
        if not crash:
            #도로 차선 이동
            for i in range(lane_count):
                pygame.draw.rect(screen, WHITE, [lanes[i][0], lanes[i][1], lane_width, lane_height])
                lanes[i][1] += 10 #도로 차선 속도
                if lanes[i][1] > WINDOW_HEIGHT:
                    lanes[i][1] = -40 - lane_height

            #사용자 레이싱 카
            player.draw_image()
            player.move_x()
            player.check_out_of_screen()

            #컴퓨터 레이싱 카
            for i in range(car_count):
                cars[i].draw_image()
                cars[i].y += cars[i].dy
                if cars[i].y > WINDOW_HEIGHT:
                    score += 10
                    cars[i].y = random.randrange(-150, -50)
                    cars[i].x = random.randrange(0, WINDOW_WIDTH-cars[i].width)
                    cars[i].dy = random.randint(4, 9)
                    cars[i].load_image()

            #레이싱 카 충돌사고 체크
            for i in range(car_count):
                if player.check_crash(cars[i]):
                    crash = True
                    pygame.mixer.music.stop()
                    sound_crash.play()
                    sleep(2)
                    pygame.mouse.set_visible(True)
                    break

            draw_score(score)
            pygame.display.flip()
        else:
            draw_main_menu(score)

        clock.tick(60)

    pygame.quit()
