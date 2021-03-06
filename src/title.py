#Basic Worm game. Uses PyGame library.

import worm_obj
import worm_fun
import pygame
from pygame.locals import *
from sys import exit
import os

#Set up everything
pygame.init()

#Set up sound
pygame.mixer.init(channels=1)
bite = pygame.mixer.Sound('bite.ogg')
pygame.mixer.music.load('goldberg.ogg')

#Set up time
clock = pygame.time.Clock()
delay = 300 #time in ms between worm's motions
pygame.time.set_timer(USEREVENT+1, delay)

#Set up screen
SCREEN_SIZE = (300, 300)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
pygame.display.set_caption("Worm")

#These variables will be used for positioning text
x = SCREEN_SIZE[0]/2 - 85
y = 2 * SCREEN_SIZE[1]/5 - 30

#Set up font
font = pygame.font.SysFont("arial", 60);
font1 = pygame.font.SysFont("arial", 20);
font_height = font.get_linesize()

#food = worm_obj.Food()
title_worm = worm_obj.TitleWorm()
state = 'title'

# Main loop
while True:
    for event in pygame.event.get():
        if state == 'title' or state == 'end':
            # Start/resume game when player presses a key
            if event.type == KEYDOWN:
                state = 'game'
                game_worm = worm_obj.Worm()
                food = worm_obj.Food()
                delay = 200
                score = 0
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play(-1, 0)
                
            elif event.type == MOUSEBUTTONDOWN:
                state = 'game'
                game_worm = worm_obj.SmartWorm()
                food = worm_obj.Food()
                delay = 200
                score = 0
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play(-1, 0)
                
        if state == 'game':
            #Move worm every [delay] ms
            if event.type == USEREVENT+1:
                game_worm.move(food)
            #Respond to keystrokes
            if event.type == KEYDOWN:
                game_worm.change_dir(food)
                
        if event.type == QUIT:
            pygame.quit()
            exit()
        
    #Color background
    screen.fill((245, 241, 222))
    
    #Title screen displays a sample worm moving around the title
    if state == 'title':
        #Dispaly title text
        screen.blit(font.render("WORM!", True, (100,100,0)),(x,y))
        screen.blit(font1.render("Press any key to play.", True, (245, 0, 20)),
                    (x + 7, y+font_height+20))
        
        #Move the worm object around the text
        pygame.time.wait(delay) 
        title_worm.get_dir()
        title_worm.move('')
        title_worm.draw(screen)
        
    elif state == 'game':
        screen.blit(font1.render(str(score), True, (0, 0, 0)),
                                 (30, SCREEN_SIZE[1] - 30))
        game_worm.draw(screen)
        food.draw(screen)
        # Run collision detection
        #This handles the case where the worm hits itself or a wall
        if game_worm.collide(food) == 'fail':
            screen.blit(font.render("FAIL", True, (100,100,0)),(x + 35,y))
            screen.blit(font1.render("Press any key to play again.", True,
                                     (245, 0, 20)), (x-10, y+font_height+20))
            screen.blit(font1.render(str(score), True, (0, 0, 0)),
                                     (30, SCREEN_SIZE[1] - 30))
            game_worm.draw(screen)
            food.draw(screen)
            pygame.display.update()
            pygame.time.delay(1000)
            state = 'end'
        #Worm collides with food
        elif game_worm.collide(food) == 'eat':
            #food = worm_obj.Food()
            game_worm.eat()
            food = worm_obj.Food()

            #Make sure food doesn't generate inside worm
            #for segment in game_worm.worm_list:
            #    while segment.outline.colliderect(food.outline):
            #        food = worm_obj.Food()
            score += 10
            delay -= 2
            pygame.time.set_timer(USEREVENT+1, delay)
            bite.play()
            
            
            
    elif state == 'end':
        screen.blit(font.render("FAIL", True, (100,100,0)),(x + 35,y))
        screen.blit(font1.render("Press any key to play again.", True,
                                 (245, 0, 20)), (x-10, y+font_height+20))
        screen.blit(font1.render(str(score), True, (0, 0, 0)),
                                 (30, SCREEN_SIZE[1] - 30))
        game_worm.draw(screen)
        food.draw(screen)

        
    pygame.display.update()

    clock.tick(30)
