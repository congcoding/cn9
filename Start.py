import gettext
import math
import random

from PySpaceship import PySpaceShip
from PyCar import racingcar
from PyShooting import PyShooting
import Ranking
import windowsC

import pygame
from pygame.locals import *

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 600
WHITE = (200, 200, 200)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

default_font = pygame.font.Font('./PySpaceship/NanumGothic.ttf', 28)

def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect) 

def main_screen():
    pygame.mouse.set_visible(True)

    start_image = pygame.image.load('main.png')
    pygame.display.set_caption('수룡 게임 천국')
    screen.blit(start_image, [0, 0])

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                PySpaceShip.main_loop()
                return 'main_screen'
            elif event.key == pygame.K_2:
                racingcar.main_loop()
                return 'main_screen'
            elif event.key == pygame.K_3:
                PyShooting.initGame()
                PyShooting.runGame()
                return 'main_screen'
            elif event.key == pygame.K_4:
                Ranking.main_loop()
                return 'main_screen'
            elif event.key == pygame.K_5:
                windowsC.main_loop()
                return 'main_screen'
        if event.type == QUIT:
            return 'quit'

    return 'main_screen'

def main_loop():
    action = 'main_screen'
    while action != 'quit':
        if action == 'main_screen':
            action = main_screen()

    pygame.quit()   

main_loop()
