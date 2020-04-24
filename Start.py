import gettext
import math
import random
import sys
from time import sleep

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

    start_image = pygame.image.load('./PySpaceship/game_screen.png')
    screen.blit(start_image, [0, 0])

    draw_text('게임 1', default_font, 
               screen, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.5, WHITE)
    draw_text('게임 2', default_font, 
               screen, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2.0, WHITE)
    draw_text('게임 3', default_font, 
               screen, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2.5, WHITE)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("keydown1")
                return 'main_screen'
            elif event.key == pygame.K_2:
                print("keydown2")
                return 'main_screen'
            elif event.key == pygame.K_3:
                print("keydown3")
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
