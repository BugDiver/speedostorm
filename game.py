# coding=UTF-8
import pygame
import time
import random

pygame.init()
carImg = pygame.image.load('racingcar.png')
pygame.display.set_icon(carImg)

display_width = 800
display_height = 900
car_width = 140

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
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


def enemy(enemy_x, enemy_y, enemy_w, enemy_h, color):
    pygame.draw.rect(gameDisplay, color, [enemy_x, enemy_y, enemy_w, enemy_h])


def enemis_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Dodged: ' + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# button (message ,button_start_x ,button_start_y ,button_width,button_height ,normal_color ,hover_color)
def button(msg, x, y, w, h, nc, hc, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    	
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, hc, (x, y, w, h))
        if click[0] == 1 and action != None:
        	action()
    else:
        pygame.draw.rect(gameDisplay, nc, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText, white)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def display_message(message, color):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurface, TextRect = text_objects(message, largeText, color)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurface, TextRect)
    pygame.display.update()

    time.sleep(2)
    game_loop()


def crash():
    display_message('You Crashed!!!', red)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects(
            "špëędôśtørm".decode("UTF-8"), largeText, black)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Go!", 150, 650, 100, 50, green, bright_green, game_loop)
        button("Quit!", 550, 650, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def unpause():
    global pause
    pause = False


def paused():
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("Paused", largeText, black)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        button("Continue", 150, 650, 100, 50, green, bright_green, unpause)
        button("Quit!", 550, 650, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_loop():
    global pause
    x = (display_width * 0.43)
    y = (display_height * 0.8)
    x_change = 0
    enemy_speed = 5
    enemy_width = 100
    enemy_height = 100
    enemy_start_x = random.randrange(0, display_width)
    enemy_start_y = -600

    dodged = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -10
                if event.key == pygame.K_RIGHT:
                    x_change = 10
                if event.key == pygame.K_SPACE:
					pause = True
					paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)

        car(x, y)
        enemy(enemy_start_x, enemy_start_y, enemy_width, enemy_height, black)
        enemy_start_y += enemy_speed
        enemis_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()
        if enemy_start_y > display_height:
            enemy_start_y = 0
            enemy_start_x = random.randrange(0, display_width - enemy_width)
            dodged += 1
            if dodged % 5 == 0:
                enemy_speed += 2

        if y < enemy_start_y + enemy_height:
            if x > enemy_start_x and x < enemy_start_x + enemy_width or x + car_width > enemy_start_x and x + car_width < enemy_start_x + enemy_width:
                crash()

        pygame.display.update()
        clock.tick(60)


game_intro()
