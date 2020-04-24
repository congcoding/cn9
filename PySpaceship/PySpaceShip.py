import gettext
import math
import random
import sys
from time import sleep

import pygame
from pygame.locals import *

WINDOW_WIDTH = 480  #800
WINDOW_HEIGHT = 600 #600

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
YELLOW = (250, 250, 20)
BLUE = (20, 20, 250)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('PySpaceShip : 우주 암석 피하기 게임')
pygame.display.set_icon(pygame.image.load('./PySpaceShip/warp.png'))
fps_clock = pygame.time.Clock()
FPS = 60
score = 0

default_font = pygame.font.Font('./PySpaceShip/NanumGothic.ttf', 28)
background_img = pygame.image.load('./PySpaceShip/background.jpg')
explosion_sound = pygame.mixer.Sound('./PySpaceShip/explosion.wav')
warp_sound = pygame.mixer.Sound('./PySpaceShip/warp.wav')
pygame.mixer.music.load('./PySpaceShip/Inner_Sanctum.mp3')

# Sprite : pygame에서 게임에서 빈번하게 발생하는 객체들을 쉽게 관리할 수 있게 상속받을 수 있는 class
class Spaceship(pygame.sprite.Sprite):  # 우주선 객체
    def __init__(self) :    # 초기화
        super(Spaceship, self).__init__()    # 상속받은 sprite에 Spaceship을 넘겨줌
        self.image = pygame.image.load('./PySpaceShip/spaceship.png')
        self.rect = self.image.get_rect()
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

    def set_pos(self, x, y):    # position 셋팅해주는 함수
        self.rect.x = x - self.centerx
        self.rect.y = y - self.centery

    def collide(self, sprites): #우주선이 다른 객체와 충돌했는지 판단하는 function을 sprite에서 가져옴
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

class Rock(pygame.sprite.Sprite): #암석 객체
    def __init__(self, xpos, ypos, hspeed, vspeed):
        super(Rock, self).__init__()
        rocks = ('./PySpaceShip/rock01.png', './PySpaceShip/rock02.png', './PySpaceShip/rock03.png', './PySpaceShip/rock04.png', './PySpaceShip/rock05.png', \
                 './PySpaceShip/rock06.png', './PySpaceShip/rock07.png', './PySpaceShip/rock08.png', './PySpaceShip/rock09.png', './PySpaceShip/rock10.png', \
                 './PySpaceShip/rock11.png', './PySpaceShip/rock12.png', './PySpaceShip/rock13.png', './PySpaceShip/rock14.png', './PySpaceShip/rock15.png', \
                 './PySpaceShip/rock16.png', './PySpaceShip/rock17.png', './PySpaceShip/rock18.png', './PySpaceShip/rock19.png', './PySpaceShip/rock20.png', \
                 './PySpaceShip/rock21.png', './PySpaceShip/rock22.png', './PySpaceShip/rock23.png', './PySpaceShip/rock24.png', './PySpaceShip/rock25.png', \
                 './PySpaceShip/rock26.png', './PySpaceShip/rock27.png', './PySpaceShip/rock28.png', './PySpaceShip/rock29.png', './PySpaceShip/rock30.png')
                 # 암석 이미지 파일 30개 입력

        self.image = pygame.image.load(random.choice(rocks)) # 30개 중에 랜덤으로 선택
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.hspeed = hspeed
        self.vspeed = vspeed

        self.set_direction()

    def set_direction(self):    # 암석의 방향에 따라 이미지를 기울여주는 함수
        if self.hspeed > 0:
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.hspeed < 0:
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.vspeed > 0:
            self.image = pygame.transform.rotate(self.image, 180)
            
    def update(self): #암석의 속도가 바뀔 때 마다 호출하는 함수
        self.rect.x += self.hspeed #이동할 때 마다 update함수를 호출하면서 화면이 계속 update되고 암석의 움직임을 갱신해줌
        self.rect.y += self.vspeed
        if self.collide():  #암석이 충돌했을 때
            self.kill()     #암석을 사라지게 함

    def collide(self):
        if self.rect.x < 0 - self.rect.height or self.rect.x > WINDOW_WIDTH:
            return True
        elif self.rect.y < 0 - self.rect.height or self.rect.y > WINDOW_HEIGHT:
            return True


def random_rock(speed): #암석이 랜덤하게 나와야 함
    random_direction = random.randint(1, 4)
                                                                                #ROCK(xpos, ypos, hspeed, vspeed)
    if random_direction == 1: #위에서 아래로 나오는 경우
        return Rock(random.randint(0, WINDOW_WIDTH), 0, 0, speed)               #xpos는 WIDTH에서 랜덤으로, ypos는 0(위), hspeed는 0(위아래로 움직이기 때문), vspeed = +speed(위에서 아래)
    elif random_direction == 2: #오른쪽에서 왼쪽으로 나오는 경우
        return Rock(WINDOW_WIDTH, random.randint(0, WINDOW_HEIGHT), -speed, 0)  #xpos는 WINDOW_WIDTH(오른쪽), ypos는 HEIGHT에서 랜덤으로, hspeed는 -speed(오른쪽에서 왼쪽), vspeed는 0
    elif random_direction == 3: # 아래에서 위로
        return Rock(random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT, 0, -speed)  #xpos는 WIDTH에서 랜덤으로, ypos는 HEIGHT(아래), hspeed는 0, vspeed = -speed(아래에서 위로)
    elif random_direction == 4: #왼쪽에서 오른쪽으로 나오는 경우
        return Rock(0, random.randint(0, WINDOW_HEIGHT), speed, 0)              #xpos는 0, vpos는 HEIGHT에서 랜덤으로, hspeed = +speed(왼쪽에서 오른쪽), vspeed = 0

class Warp(pygame.sprite.Sprite):   #Warp 아이템 : spaceship과 동
    def __init__(self, x, y):
        super(Warp, self).__init__()
        self.image = pygame.image.load('./PySpaceShip/warp.png')
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.centerx
        self.rect.y = y - self.rect.centery

        
def draw_repeating_background(background_img): #배경 이미지 반복하는 함수
    background_rect = background_img.get_rect() #WIDTH / 배경이미지 width한 후 올림
    for i in range(int(math.ceil(WINDOW_WIDTH / background_rect.width))):
        for j in range(int(math.ceil(WINDOW_HEIGHT / background_rect.height))):
            screen.blit(background_img, Rect(i * background_rect.width, #전체 width
                                             j * background_rect.height, #전체 height
                                             background_rect.width, #배경이미지 width
                                             background_rect.height)) #배경이미지 height

def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)   #36분 48초 : 텍스트가 어떤 font에 어떤 text를 이 surface에다가 blit해줘 그런데 그거에 대해서 우리가 메인 컬러로 렌더링한 값으로 넣어주는 함수


def game_loop():    #실제 게임 엔진
    global score

    pygame.mixer.music.play(-1) #게임 배경음악 무한반복
    pygame.mouse.set_visible(False) #마우스 포인터 안보이게 하는 것 (마우스 모양이 우주선으로 바뀌어 있으므로)

    spaceship = Spaceship()
    spaceship.set_pos(*pygame.mouse.get_pos())   #*은 가변의미, 마우스의 현재 위치가 우주선의 현재 위치가 됨
    rocks = pygame.sprite.Group()   #암석을 sprite를 사용해 그룹으로 관리
    warps = pygame.sprite.Group()   #워프를 sprite를 사용해 그룹으로 관리
    
    min_rock_speed = 1  #암석 최소 속도
    max_rock_speed = 1  #암석 최대 속도
    occur_of_rocks = 1  #암석을 보낼 때 몇 개씩 보낼지 (score가 높아지면 난이도 증가)
    occur_prob = 15     #암석 발생 확률
    score = 0
    warp_count = 1
    paused = False #p버튼을 누르면 일시정지할 수 있게 하는 기능

    while True:
        pygame.display.update() #게임 화면이 계속 update되어야 하므로
        fps_clock.tick(FPS)     #fps를 전역으로 선언해놓은 FPS=60으로 설정

        if paused:
            for event in pygame.event.get(): 
                if event.type == pygame.KEYDOWN:    #키를 누르는 event 가져오기
                    if event.key == pygame.K_p:     #눌러진 키가 p면
                        paused = not paused         #paused를 toggle
                        pygame.mouse.set_visible(False)     #마우스를 안보이게
                if event.type == QUIT:  #42:27 event가 QUIT일 때?
                    return 'quit'
        else:
            draw_repeating_background(background_img)

            occur_of_rocks = 1 + int(score / 500) #난이도와 관련
            min_rock_speed = 1 + int(score / 400)
            max_rock_speed = 1 + int(score / 300)
    
        if random.randint(1, occur_prob) == 1:
            for i in range(occur_of_rocks):
                rocks.add(random_rock(random.randint(min_rock_speed, max_rock_speed)))
                score += 1 #암석이 하나 증가되면 score + 1

            if random.randint(1, occur_prob * 5) == 1: #warp가 생길 확률을 1/150(10일때, 너무 안나와서 5로 바꿈)으로 설정
                warp = Warp(random.randint(30, WINDOW_WIDTH - 30),
                            random.randint(30, WINDOW_HEIGHT - 30)) #너무 가장자리에 나오면 안되므로 margin 설정
                warps.add(warp)

        draw_text('점수: {}'.format(score), default_font, screen, 80, 20, YELLOW) # 점수 출력
        draw_text('워프: {}'.format(warp_count), default_font, screen, 380, 20, BLUE)
        rocks.update()
        warps.update()
        rocks.draw(screen)
        warps.draw(screen)

        warp = spaceship.collide(warps) #elif에서 쓰려고 변수화
        if spaceship.collide(rocks):    #암석과 우주선이 충돌하면
            explosion_sound.play()      #충돌 사운드 출력
            pygame.mixer.music.stop()   #게임이 끝나기 전에 음악 중단
            rocks.empty()               #전체 암석을 없애고
            return 'game_screen'        #game_screen으로 돌아감
        elif warp: #워프에 우주선이 닿으면 아이템 획득의 의미
            warp_count += 1  #워프의 개수를 증가시키고      
            warp.kill()      #워프 이미지 없애

        screen.blit(spaceship.image, spaceship.rect)

        # 여기까지 화면 업데이트 부분, 아래부터 컨트롤 부분

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] <= 10:  #mouse가 왼쪽으로 나가면(mouse_pos[0] = 마우스의 x좌표)
                    pygame.mouse.set_pos(WINDOW_WIDTH - 10, mouse_pos[1])   #오른쪽에서 등장, y값은 그대로 사용 (mouse_pos[1] = 마우스의 y좌표)
                elif mouse_pos[0] >= WINDOW_WIDTH - 10: #mouse가 오른쪽으로 나가면
                    pygame.mouse.set_pos(0 + 10, mouse_pos[1]) #왼쪽에서 등장 (10은 모두 약간의 공간)
                elif mouse_pos[1] <= 10: #mouse가 위로 나가면(pygame좌표 기준점은 왼쪽 위)
                    pygame.mouse.set_pos(mouse_pos[0], WINDOW_HEIGHT - 10) #아래에서 등장
                elif mouse_pos[1] >= WINDOW_HEIGHT - 10:
                    pygame.mouse.set_pos(mouse_pos[0], 0 + 10)
                spaceship.set_pos(*mouse_pos)   #spaceship에 실제적인 mouse의 pos를 전달
            if event.type == pygame.MOUSEBUTTONDOWN: #왼쪽, 오른쪽 상관없이 버튼이 눌렸을 때
                if warp_count > 0:  #워프가 있으면
                    warp_count -= 1     #워프를 사용하므로 -1
                    warp_sound.play()   #워프 사운드
                    sleep(1)    #전환을 위해 약간 지연
                    rocks.empty()   #워프했으니 암석을 모두 제거
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:     #p를 누르면
                    paused = not paused     #p를 토글
                    if paused:  #일시정지 상태이면
                        transp_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)) #화면 크기만큼
                        transp_surf.set_alpha(150) #150정도 주면 불투명해짐
                        screen.blit(transp_surf, transp_surf.get_rect())
                        pygame.mouse.set_visible(True) #일시정지 상태이면 마우스 모양이 우주선에서 마우스로 바뀜
                        draw_text('일시정지',
                                  pygame.font.Font('./PySpaceShip/NanumGothic.ttf', 60),
                                  screen, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, YELLOW) #가운데에 일시정지 글씨 표시
            if event.type == QUIT: #QUIT이벤트가 발생하면 QUIT
                return 'quit'
            
    return 'game_screen' #end while -> screen으로 이동


def game_screen():
    global score
    pygame.mouse.set_visible(True)

    start_image = pygame.image.load('./PySpaceShip/game_screen.png')
    screen.blit(start_image, [0, 0])

    draw_text('우주 암석 피하기',
              pygame.font.Font('./PySpaceShip/NanumGothic.ttf', 50), screen,
              WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3.0, WHITE)
    draw_text('마우스 버튼이나 "1"키를 누르면 게임이 시작됩니다.',
              pygame.font.Font('./PySpaceShip/NanumGothic.ttf', 20), screen,
              WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2.3, WHITE)
    draw_text('점수: {}'.format(score),
              default_font, screen,
              WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2.0, YELLOW)    


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return 'quit'
            elif event.key == pygame.K_0:
                import Start
                Start.main_loop()
            elif event.key == pygame.K_1:
                return 'play'
        if event.type == pygame.MOUSEBUTTONDOWN:
            return 'play'
        if event.type == QUIT:
            return 'quit'

    return 'game_screen'

def main_loop(): #main_loop로 액션을 취해줌
    action = 'game_screen'
    while action != 'quit':
        if action == 'game_screen':
            action = game_screen()
        elif action == 'play':
            action = game_loop()

    pygame.quit()
