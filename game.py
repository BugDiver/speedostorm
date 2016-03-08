# coding=UTF-8
import pygame
import random

pygame.init()
carImg = pygame.image.load('racingcar.png')
enmy_img = pygame.image.load('enemycar.png')
pygame.display.set_icon(carImg)

crash_sound = pygame.mixer.Sound('crashed.wav');
pygame.mixer.music.load('playback.wav')

display_width = 800
display_height = 900
car_width = 140

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
blue = (0,0,200)


green = (0, 116, 0)
bright_red = (255, 0, 0)
bright_green = (0, 200, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('SpeedoStorm')

clock = pygame.time.Clock()

pause = False

def quit_game():
    pygame.quit()
    quit()


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


def enemy(enemy_x, enemy_y):
    gameDisplay.blit(enmy_img, (enemy_x, enemy_y))
    # pygame.draw.rect(gameDisplay, color, [enemy_x, enemy_y, enemy_w, enemy_h])


def enemis_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Dodged: ' + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def onClick(action):
    click = pygame.mouse.get_pressed()
    if click[0] == 1 and action != None:
        action()

# button (message ,button_start_x ,button_start_y ,button_width,button_height ,normal_color ,hover_color)
def button(msg, x, y, w, h, nc, hc, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()  	
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, hc, [x, y, w, h])
        onClick(action)
    else:
        pygame.draw.rect(gameDisplay, nc, (x, y, w, h))
    printText(msg ,white ,((x + (w / 2)), (y + (h / 2))) ,20)


def printText(text ,color,position,size):
    largeText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(text.decode("UTF-8"), largeText, color)
    TextRect.center = position
    gameDisplay.blit(TextSurf, TextRect)

def showButtons(btn1,btn2):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        gameDisplay.fill(white)
        printText("špëędôśtørm",black,((display_width / 2), (display_height / 2)),115)

        button(btn1['msg'], 150, 650, 100, 50, green, bright_green, btn1['action'])
        button(btn2['msg'], 550, 650, 100, 50, red, bright_red, btn2['action'])

        pygame.display.update()
        clock.tick(15)

def crash():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    printText('You Crashed!!' ,red,((display_width / 2), (display_height / 2)),115)
    btn1 = {'msg' : 'play again' ,'action' : game_loop}
    btn2 = {'msg' : 'Quit!' ,'action' : quit_game}
    showButtons(btn1,btn2)
    

def initialize_game():
    btn1 = {'msg' : 'Go!' ,'action' : game_loop}
    btn2 = {'msg' : 'Quit!' ,'action' : quit_game}
    showButtons(btn1,btn2)

def unpause():
    global pause
    pause = False
    pygame.mixer.music.unpause()

def paused():
    global pause
    pygame.mixer.music.pause()
    printText('Paused' ,black,((display_width / 2), (display_height / 2)),115)
    btn1 = {'msg' : 'Continue' ,'action' : unpause}
    btn2 = {'msg' : 'Quit!' ,'action' : quit_game}
    showButtons(btn1,btn2)

def game_loop():
    global pause
    pygame.mixer.music.play(-1)
    x = (display_width * 0.43)
    y = (display_height * 0.75)
    x_change = 0
    enemy_speed = 5
    enemy_width = 100
    enemy_height = 250
    enemy_start_x = random.randrange(0, display_width)
    enemy_start_y = -600

    dodged = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_UP:
                    enemy_speed+=5
                if event.key == pygame.K_SPACE:
					pause = True
					paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP:
                    enemy_speed -= 5

        x += x_change
        gameDisplay.fill(white)

        enemy(enemy_start_x, enemy_start_y)
        enemy_start_y += enemy_speed
        enemis_dodged(dodged)
        car(x, y)

        if x > display_width - car_width or x < 0:
            crash()
        if enemy_start_y > display_height:
            enemy_start_y = -enemy_height
            enemy_start_x = random.randrange(0, display_width - enemy_width + 10)
            dodged += 1
            if dodged % 5 == 0:
                enemy_speed += 2

        if y < enemy_start_y + enemy_height:
            if x > enemy_start_x and x < enemy_start_x + enemy_width or x+car_width > enemy_start_x and x + car_width < enemy_start_x+enemy_width:
                crash()

        pygame.display.update()
        clock.tick(120)


initialize_game()
