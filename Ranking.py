import gettext
import math
import random
import pickle
import cx_Oracle
from operator import itemgetter

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

    ################ 우주에서 살아남기 랭킹 ################
    # 파일에서 점수 정보 가져오기
    draw_text("우주에서 살아남기(Local)", default_font, screen, 120, 150,  BLACK)
    try:
        PySpaceshipLocalRankingList = pickle.load(open("./PySpaceship/PySpaceshipRanking.pic", "rb"))
    except:
        PySpaceshipLocalRankingList = []
    PySpaceshipLocalRankingList.sort(key=itemgetter(1), reverse=True)
    length = len(PySpaceshipLocalRankingList)
    if length > 4:
        length = 4
    for i in range(0, length):
        draw_text(str(PySpaceshipLocalRankingList[i][0]), default_font, screen, 90, 180 + (i * 30),  BLACK)
        draw_text(str(PySpaceshipLocalRankingList[i][1]), default_font, screen, 140, 180 + (i * 30),  BLACK)
    
    # DB에서 점수 정보 가져오기
    draw_text("우주에서 살아남기(Online)", default_font, screen, 360, 150,  BLACK)
    try :
        conn = cx_Oracle.connect("shy/shyshyshy@kh-final.c9kbkjh06ivh.ap-northeast-2.rds.amazonaws.com:1521/shy") # DB 연결
        cursor = conn.cursor()  # cursor 가져오기
        cursor.execute("select * from ranking where gamecode = 1 order by score desc") # 쿼리 실행
        PySpaceshipOnlineRankingList = cursor.fetchall() # 조회 결과를 list에 저장
        conn.commit()   # commit
        cursor.close()  # cursor 닫기
        conn.close()    # 연결 close 하기
    
        length = len(PySpaceshipOnlineRankingList)
        if length > 4:  # 최대 4개의 ranking 점수만 가져오기 위해 랭킹 정보가 4개보다 많은 경우 length를 4로 설정
            length = 4
        for i in range(0, length):  # 상위 4개의 점수를 화면에 출력하기
            draw_text(str(PySpaceshipOnlineRankingList[i][1]), default_font, screen, 330, 180 + (i * 30),  BLACK)
            draw_text(str(PySpaceshipOnlineRankingList[i][2]), default_font, screen, 390, 180 + (i * 30),  BLACK)
    except :
        # DB에 연결 시도했는데 실패할 경우 온라인 랭킹에 "인터넷에 연결할 수 없습니다"를 화면에 출력하기
        draw_text("인터넷에 연결할 수 없습니다.", default_font, screen, 360, 180,  BLACK)

    #<PyCar 점수>
    # 파일에서 점수 정보 가져오기
    draw_text("수룡이의 레이싱(Local)", default_font, screen, 120, 300,  BLACK)
    try:
        PyCarLocalRankingList = pickle.load(open("./PyCar/PyCarRanking.pic", "rb"))
    except:
        PyCarLocalRankingList = []            
    PyCarLocalRankingList.sort(key=itemgetter(1), reverse=True)
    if len(PyCarLocalRankingList) >= 4:
        for i in range(0, 4):
            draw_text(str(PyCarLocalRankingList[i][0]), default_font, screen, 90, 330 + (i * 30),  BLACK)
            draw_text(str(PyCarLocalRankingList[i][1]), default_font, screen, 140, 330 + (i * 30),  BLACK)
    else:
        for i in range(0, len(PyCarLocalRankingList)):
            draw_text(str(PyCarLocalRankingList[i][0]), default_font, screen, 90, 330 + (i * 30),  BLACK)
            draw_text(str(PyCarLocalRankingList[i][1]), default_font, screen, 140, 330 + (i * 30),  BLACK)

    # DB에서 점수 정보 가져오기
    draw_text("수룡이의 레이싱(Online)", default_font, screen, 360, 300,  BLACK)
    try:
        connection = cx_Oracle.connect("shy/shyshyshy@kh-final.c9kbkjh06ivh.ap-northeast-2.rds.amazonaws.com:1521/shy")
        cursor = connection.cursor()
        cursor.execute("select * from ranking where gamecode = 2 order by score desc")
        PyCarOnlineRankingList = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        if len(PyCarOnlineRankingList) >= 4:
            for i in range(0, 4):
                draw_text(str(PyCarOnlineRankingList[i][2]), default_font, screen, 390, 330 + (i * 30),  BLACK)
                draw_text(str(PyCarOnlineRankingList[i][1]), default_font, screen, 330, 330 + (i * 30),  BLACK)
        else:
            for i in range(0, len(PyCarOnlineRankingList)):
                draw_text(str(PyCarOnlineRankingList[i][2]), default_font, screen, 390, 330 + (i * 30),  BLACK)
                draw_text(str(PyCarOnlineRankingList[i][1]), default_font, screen, 330, 330 + (i * 30),  BLACK)
    except:
        draw_text("인터넷에 연결할 수 없습니다.", default_font, screen, 360, 330,  BLACK)


    # 3번 게임 랭킹 ************************************************************
    # 파일에서 로컬 점수 가져오기
    draw_text("학교를 지켜라(Local)", default_font, screen, 120, 450,  BLACK)
    try:
        PyShootingLocalRankingList = pickle.load(open("./PyShooting/PyShootingRanking.pic", "rb")) # 피클 모듈을 통해 저장된 점수 불러와 리스트에 넣기
    except:
         PyShootingLocalRankingList = [] # 기존에 저장된 점수가 없을 경우 빈 리스트 만들기
    PyShootingLocalRankingList.sort(key=itemgetter(1), reverse=True) # 이름/점수로 구성된 2차원 리스트를 점수를 기준으로 내림차순으로 정렬
    if len(PyShootingLocalRankingList) >= 4: # 가장 높은 점수 4개 까지만 출력
        for i in range(0, 4):
            draw_text(str(PyShootingLocalRankingList[i][0]), default_font, screen, 90, 480 + (i * 30),  BLACK) # 이름 출력
            draw_text(str(PyShootingLocalRankingList[i][1]), default_font, screen, 140, 480 + (i * 30),  BLACK) # 점수 출력
    else:
        for i in range(0, len(PyShootingLocalRankingList)):
            draw_text(str(PyShootingLocalRankingList[i][0]), default_font, screen, 90, 480 + (i * 30),  BLACK)
            draw_text(str(PyShootingLocalRankingList[i][1]), default_font, screen, 140, 480 + (i * 30),  BLACK)
            
    # DB에서 온라인 점수 가져오기
    draw_text("학교를 지켜라(Online)", default_font, screen, 360, 450,  BLACK)
    try:
        conn = cx_Oracle.connect("shy/shyshyshy@kh-final.c9kbkjh06ivh.ap-northeast-2.rds.amazonaws.com:1521/shy")
        cursor = conn.cursor()
        cursor.execute("select * from ranking where gamecode = 3 order by score desc")
        PyShootingOnlineRankingList = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        if len(PyShootingOnlineRankingList) >= 4:
            for i in range(0, 4):
                draw_text(str(PyShootingOnlineRankingList[i][2]), default_font, screen, 390, 480 + (i * 30),  BLACK)
                draw_text(str(PyShootingOnlineRankingList[i][1]), default_font, screen, 330, 480 + (i * 30),  BLACK)
        else:
            for i in range(0, len(PyShootingOnlineRankingList)):
                draw_text(str(PyShootingOnlineRankingList[i][2]), default_font, screen, 390, 480 + (i * 30),  BLACK)
                draw_text(str(PyShootingOnlineRankingList[i][1]), default_font, screen, 330, 480 + (i * 30),  BLACK)
    except:
        draw_text("인터넷에 연결할 수 없습니다.", default_font, screen, 360, 480,  BLACK)

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
