#-*- encoding: utf-8 -*-

import gettext
import pygame
from pygame.locals import *
import random
from time import sleep
import pickle
import cx_Oracle
import os
os.putenv('NLS_LANG', '.UTF8')

import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from tkinter import *
from tkinter import messagebox

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 600

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
default_font = pygame.font.Font('./PyCar/NanumGothic.ttf', 28)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
MAIN = (239, 218, 255)

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

def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect) 

def draw_main_menu(score):
    screen.fill(WHITE)
    draw_x = (WINDOW_WIDTH / 2) - 200
    draw_y = WINDOW_HEIGHT / 2
    image_flag = pygame.image.load('./PyCar/flag.png')
    screen.blit(image_flag, [0, 0])

    image_intro = pygame.image.load('./PyCar/PyCar2.png')
    screen.blit(image_intro, [draw_x + 40, draw_y - 280])
    font_40 = pygame.font.SysFont("FixedSys", 40, True, False)
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)

    draw_text('카레이서 수룡이의 레이싱!',
              pygame.font.Font('./PyCar/NanumGothic.ttf', 35), screen,
              draw_x+200, draw_y+10, BLACK)
    score_text = font_40.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, [draw_x, draw_y + 70])

    draw_text('수룡이가 레이싱에서 이길 수 있게 도와주세요~',
              pygame.font.Font('./PyCar/NanumGothic.ttf', 20), screen,
              draw_x+200, draw_y+60, BLACK)
    draw_text('방향키를 이용해 자동차를 피해주세요',
              pygame.font.Font('./PyCar/NanumGothic.ttf', 15), screen,
              draw_x+200, draw_y+100, (19, 2, 171))
    draw_text('시작하려면 스페이스 키를 누르세요',
              pygame.font.Font('./PyCar/NanumGothic.ttf', 15), screen,
              draw_x+200, draw_y+130, (19, 2, 171))
    draw_text('나가려면 0을 누르세요',
              pygame.font.Font('./PyCar/NanumGothic.ttf', 15), screen,
              draw_x+200, draw_y+155, (19, 2, 171))
    pygame.display.flip()

def draw_score(score):
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    txt_score = font_30.render("Score: " + str(score), True, BLACK)
    screen.blit(txt_score, [15, 15])  

def main_loop():
    pygame.init()

    pygame.display.set_caption("카레이서 수룡이의 레이싱!")
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
                    sleep(3)
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
                    # name 입력하는 부분
                    root = Tk()

                    # 버튼 클릭 이벤트 핸들러
                    def okClick():
                        name = txt.get()
                        try:
                            # DB를 이용해 score 저장
                            conn = cx_Oracle.connect("shy/shyshyshy@kh-final.c9kbkjh06ivh.ap-northeast-2.rds.amazonaws.com:1521/shy")
                            cursor = conn.cursor()
                            if len(name)==0:
                                messagebox.showinfo("완료", "이름 없이 저장되었습니다")
                                name = "익명"
                            else:
                                messagebox.showinfo("완료", "저장되었습니다")
                            cursor.execute("insert into ranking(gamecode, name, score) values ('%d', '%s', '%d')" % (2, name[:5], score))
                            conn.commit()
                            cursor.close()
                            conn.close()
                        except:
                            messagebox.showerror("경고", "인터넷에 연결되어 있지 않아 로컬에만 저장되었습니다.")

                        # 로컬에 등록
                        try: 
                            PyCarRankingList = pickle.load(open("./PyCar/PyCarRanking.pic", "rb"))
                        except:
                            PyCarRankingList = []

                        tmpList = []
                        tmpList.append(name)
                        tmpList.append(score)
                        PyCarRankingList.append(tmpList)
                        pickle.dump(PyCarRankingList, open("./PyCar/PyCarRanking.pic", "wb"))

                        root.destroy()

                    root.title('이름 입력') # 타이틀
                    root.geometry('230x60+190+350')
                    
                    lbl = Label(root, text="이름(최대 5글자)")
                    lbl.grid(row=0, column=0)
                    txt = Entry(root)
                    txt.grid(row=0, column=1)
                    btn = Button(root, text="OK", width=15, command=okClick)
                    btn.grid(row=1, column=1)
                    
                    root.mainloop()

                    # 한글 설정
                    os.putenv('NLS_LANG', '.UTF8')
                    
                    # pickle을 이용해 파일에 score 저장
                    #try:
                    #    PyCarRankingList = pickle.load(open("./PyCar/PyCarRanking.pic", "rb"))
                    #except:
                    #    PyCarRankingList = []
                    #PyCarRankingList.append(score)
                    #pickle.dump(PyCarRankingList, open("./PyCar/PyCarRanking.pic", "wb"))
                    
                    sleep(1)
                    pygame.mouse.set_visible(True)
                    break

            draw_score(score)
            pygame.display.flip()
        else:
            draw_main_menu(score)

        clock.tick(60)

    pygame.quit()
