import pygame
import sys
import random
import pickle
import cx_Oracle
from time import sleep
import os
os.putenv('NLS_LANG', '.UTF8')
from tkinter import *
from tkinter import messagebox


padWidth = 480
padHeight = 600
rockImage =['./PyShooting/newRock.png']
"""
            './PyShooting/rock01.png','./PyShooting/rock02.png','./PyShooting/rock03.png','./PyShooting/rock04.png','./PyShooting/rock05.png',\
             './PyShooting/rock06.png','./PyShooting/rock07.png','./PyShooting/rock08.png','./PyShooting/rock09.png','./PyShooting/rock10.png',\
             './PyShooting/rock11.png','./PyShooting/rock12.png','./PyShooting/rock13.png','./PyShooting/rock14.png','./PyShooting/rock15.png',\
             './PyShooting/rock16.png','./PyShooting/rock17.png','./PyShooting/rock18.png','./PyShooting/rock19.png','./PyShooting/rock20.png',\
             './PyShooting/rock21.png','./PyShooting/rock22.png','./PyShooting/rock23.png','./PyShooting/rock24.png','./PyShooting/rock25.png',\
             './PyShooting/rock26.png','./PyShooting/rock27.png','./PyShooting/rock28.png','./PyShooting/rock29.png','./PyShooting/rock30.png']
             """
explosionSound = ['./PyShooting/explosion01.wav','./PyShooting/explosion02.wav','./PyShooting/explosion03.wav','./PyShooting/explosion04.wav']



    
def writeScore(count):
    global gamePad
    # 최고 기록 출력
    """
    try:
        conn = cx_Oracle.connect("shy/shyshyshy@kh-final.c9kbkjh06ivh.ap-northeast-2.rds.amazonaws.com:1521/shy")
        cursor = conn.cursor()
        cursor.execute("select * from ranking where gamecode = 3 order by score desc")
        PyShootingOnlineRankingList = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        top = str(PyShootingOnlineRankingList[0][2])
    except:
        top = '0'
    """
    
    font = pygame.font.Font('./PyShooting/NanumGothic.ttf', 20)
    text = font.render('파괴한 운석:' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))


def writePassed(count):
    global gamePad
    font = pygame.font.Font('./PyShooting/NanumGothic.ttf', 20)
    text = font.render('놓친 운석:' + str(count) + '/3', True, (255, 0, 0))
    gamePad.blit(text, (360, 0))

def writeMenu():
    global gamePad
    font = pygame.font.Font('./PyShooting/NanumGothic.ttf', 15)
    text = font.render('메인으로 "0" 다시 시작하기 "1"', True, (100, 100, 100))
    gamePad.blit(text, (10, 25))


def writeMessage(text, count):
    global gamePad, gameOverSound

    # 게임 끝 메시지 출력
    textfont = pygame.font.Font('./PyShooting/NanumGothic.ttf', 15)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(1)


def ranking(count): # 랭킹 등록 함수
    # DB에 등록 (name 입력하는 부분)
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
            cursor.execute("insert into ranking(gamecode, name, score) values ('%d', '%s', '%d')" % (3, name[:5], count))
            conn.commit()
            cursor.close()
            conn.close()
        except:
            messagebox.showerror("경고", "인터넷에 연결되어 있지 않아 로컬에만 저장되었습니다.")

         # 로컬에 등록
        try: 
            PyShootingRankingList = pickle.load(open("./PyShooting/PyShootingRanking.pic", "rb"))
        except:
             PyShootingRankingList = []

        secondList = []
        secondList.append(name)
        secondList.append(count)
        PyShootingRankingList.append(secondList)
        pickle.dump(PyShootingRankingList, open("./PyShooting/PyShootingRanking.pic", "wb"))


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

    pauseGame()


def pauseGame(): # 게임 종료 후 0,1 선택하는 함수
    while True:
        event = pygame.event.wait()
        if event.type in [pygame.QUIT]:
            pygame.quit()
            sys.exit()
        if event.type in [pygame.KEYDOWN]: # 실행은 잘 되는데 쉘에 오류 뜸
            if event.key == pygame.K_0:
                import Start
                Start.main_loop()
            elif event.key == pygame.K_1:
                pygame.mixer.music.play(-1)
                runGame()
                

def crash(count):
    global gamePad
    writeMessage('전투기 파괴! 메인으로 "0" 다시 시작하기 "1"', count)

def gameOver(count):
    global gamePad
    writeMessage('게임 오버! 메인으로 "0" 다시 시작하기 "1"', count)

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x,y))


def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('학교를 지켜라')
    background = pygame.image.load('./PyShooting/untitled.png') # 배경
    fighter = pygame.image.load('./PyShooting/fighter.png')
    missile = pygame.image.load('./PyShooting/missile.png')
    explosion = pygame.image.load('./PyShooting/explosion.png')
    pygame.mixer.music.load('./PyShooting/music.wav')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('./PyShooting/missile.wav')
    gameOverSound = pygame.mixer.Sound('./PyShooting/gameover.wav')
    clock = pygame.time.Clock()


def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound

    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.45
    y = padHeight * 0.85
    fighterX = 0

    
    missileXY = []

    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    isShot = False
    shotCount = 0
    rockPassed = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                     fighterX -= 5
                elif event.key == pygame.K_RIGHT:
                    fighterX += 5

                elif event.key == pygame.K_SPACE:
                    missileSound.play()
                    missileX = x + fighterWidth/2 # 수정구 발사 위치 조정
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])

                if event.key == pygame.K_0: # 실행은 잘 되는데 쉘에 오류 뜸
                    pygame.mixer.music.stop()
                    import Start
                    Start.main_loop()

                elif event.key == pygame.K_1:
                    pygame.mixer.music.play(-1)
                    runGame()

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        drawObject(background, 0, 0)

        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        #운석과 충돌
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or (rockX + rockWidth > x and rockX + rockWidth <  x + fighterWidth):
                crash(shotCount) # 게임 종료
                ranking(shotCount)

        drawObject(fighter, x, y)

        if len(missileXY) !=0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]

                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass

        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx - 20, by) # 수정구 발사 위치 조정

        writeMenu()
        writeScore(shotCount)


        rockY += rockSpeed

        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        if rockPassed == 3: # 게임 종료
            gameOver(shotCount)
            ranking(shotCount)

        writePassed(rockPassed)

            

        if isShot:
            drawObject(explosion, rockX, rockY)
            destroySound.play()
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            #속도 증가
            rockSpeed += 0.2
            if rockSpeed >= 10:
                rockSpeed = 10

        drawObject(rock, rockX, rockY)
            
        pygame.display.update()

        clock.tick(60)

    pygame.quit()
