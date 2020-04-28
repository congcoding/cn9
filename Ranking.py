import gettext
import math
import random
import pickle
import cx_Oracle

import pygame
from pygame.locals import *

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 600
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

default_font = pygame.font.Font('./PySpaceship/NanumGothic.ttf', 15)


def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect) 

def ranking_screen():
    pygame.mouse.set_visible(True)

    start_image = pygame.image.load('ranking.png')
    screen.blit(start_image, [0, 0])

    # 파일에서 점수 정보 가져오기
    draw_text("PySpaceship(Local)", default_font, screen, 120, 130,  BLACK)
    PySpaceshipLocalRankingList = pickle.load(open("./PySpaceship/PySpaceshipRanking.pic", "rb"))
    PySpaceshipLocalRankingList.sort(reverse=True)
    for i in range(0, 5):
        draw_text(str(PySpaceshipLocalRankingList[i]), default_font, screen, 120, 150 + (i * 30),  BLACK)
    # DB에서 점수 정보 가져오기
    draw_text("PySpaceship(Online)", default_font, screen, 360, 130,  BLACK)
    conn = cx_Oracle.connect("shy/shyshyshy@kh-final.c9kbkjh06ivh.ap-northeast-2.rds.amazonaws.com:1521/shy")
    cursor = conn.cursor()
    cursor.execute("select * from pyspaceship order by score desc")
    PySpaceshipOnlineRankingList = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    for i in range(0, 5):
        draw_text(str(PySpaceshipOnlineRankingList[i][0]), default_font, screen, 360, 150 + (i * 30),  BLACK)

    #<PyCar 점수>
    # 파일에서 점수 정보 가져오기
    draw_text("수룡이의 레이싱(Local)", default_font, screen, 120, 300,  BLACK)
    PyCarLocalRankingList = pickle.load(open("./PyCar/PyCarRanking.pic", "rb"))
    PyCarLocalRankingList.sort(reverse=True)
    for i in range(0, 5):
        draw_text(str(PyCarLocalRankingList[i]), default_font, screen, 120, 330 + (i * 30),  BLACK)
    # DB에서 점수 정보 가져오기
    draw_text("수룡이의 레이싱(Online)", default_font, screen, 360, 300,  BLACK)
    connection = cx_Oracle.connect("shy/shyshyshy@kh-final.c9kbkjh06ivh.ap-northeast-2.rds.amazonaws.com:1521/shy")
    cursor = connection.cursor()
    cursor.execute("select * from pycar order by score desc")
    PyCarOnlineRankingList = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    for i in range(0, 5):
        draw_text(str(PyCarOnlineRankingList[i][0]), default_font, screen, 360, 330 + (i * 30),  BLACK)


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                import Start
                Start.main_loop()
                return 'ranking_screen'
        if event.type == QUIT:
            return 'quit'

    return 'ranking_screen'

def main_loop():
    action = 'ranking_screen'
    while action != 'quit':
        if action == 'ranking_screen':
            action = ranking_screen()

    pygame.quit() 
