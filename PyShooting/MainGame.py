#메인 파일입니다.
#첫 화면에서 키보드(1,2,3)를 누르면 각 게임으로 연결되도록
import PyShooting
import pygame



padwidh


def initGame():
    glodbal gamePad, background
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('background.png')


def runGame():
    global gamaPad, background

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN]: #왼쪽 키면 게임 시작, 오른쪽 키면
                
