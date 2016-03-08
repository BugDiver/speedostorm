import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 900
car_width  = 140

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)



gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('SpeedoStorm')

clock = pygame.time.Clock()
carImg = pygame.image.load('racingcar.png')

def car(x,y):
	gameDisplay.blit(carImg ,(x,y))

def enemy(enemy_x,enemy_y,enemy_w,enemy_h,color):
	pygame.draw.circle(gameDisplay ,color ,[enemy_x,enemy_y,enemy_w,enemy_h])
	

def text_objects(text ,font):
	textSurface = font.render(text ,True ,red)
	return textSurface,textSurface.get_rect()

def display_message(message):
	largeText = pygame.font.Font('freesansbold.ttf',115)
	TextSurface ,TextRect = text_objects(message ,largeText)
	TextRect.center  =((display_width /2),(display_height /2))
	gameDisplay.blit(TextSurface ,TextRect)
	pygame.display.update()

	time.sleep(2)
	game_loop()

def crash():
	display_message('You Crashed!!!')

def game_loop():
	x = (display_width * 0.43)
	y  =(display_height * 0.8)
	x_change = 0
	enemy_start_x = random.randrange(0,display_width)
	enemy_start_y = -600
	enemy_speed  = 10
	enemy_width = 100
	enemy_height = 100


	gameExit = False

	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -5
				if event.key == pygame.K_RIGHT:
					x_change = 5
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0
					
				
		x += x_change
		gameDisplay.fill(white)


		car(x,y)

		enemy(enemy_start_x,enemy_start_y ,enemy_width ,enemy_height ,black)
		enemy_start_y += enemy_speed

		if x > display_width -car_width or x < 0:
			crash()
		if enemy_start_y > display_height:
			enemy_start_y = -enemy_height
			enemy_start_x = random.randrange(0,display_width)
		pygame.display.update()
		clock.tick(60)


game_loop()
pygame.quit()
quit()
