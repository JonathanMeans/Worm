#This program displays the events
import worm_obj
background_image_filename = 'background.jpg'
mouse_image_filename = 'mouse.jpg'

import pygame
from pygame.locals import *
from sys import exit
import os

pygame.init()
pygame.mixer.init(channels=1)

clock = pygame.time.Clock()

SCREEN_SIZE = (300, 300)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
testname = os.path.join('Worm', 'bite.wav')
pygame.display.set_caption("Worm")

font = pygame.font.SysFont("arial", 60);
font1 = pygame.font.SysFont("arial", 20);
font_height = font.get_linesize()
title_worm = worm_obj.TitleWorm()

bite = pygame.mixer.Sound('bite.ogg')
delay = 300
pygame.time.set_timer(USEREVENT+1, delay)
pygame.mixer.music.load('goldberg.ogg')

state = 'title'
food = worm_obj.Food()

while True:
    for event in pygame.event.get():
        if state == 'title' or state == 'end':
            if event.type == KEYDOWN:
                state = 'game'
                game_worm = worm_obj.Worm()
                food = worm_obj.Food()
                delay = 200
                score = 0
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play(-1, 0)
        if state == 'game':
            if event.type == USEREVENT+1:
                game_worm.move()
            if event.type == KEYDOWN:
                game_worm.change_dir()
        if event.type == QUIT:
            pygame.quit()
            exit()
        
    screen.fill((245, 241, 222))
    x = SCREEN_SIZE[0]/2 - 85
    y = 2 * SCREEN_SIZE[1]/5 - 30

    if state == 'title':
        screen.blit(font.render("WORM!", True, (100,100,0)),(x,y))
        screen.blit(font1.render("Press any key to play.", True, (245, 0, 20)),
                    (x + 7, y+font_height+20))
        pygame.time.wait(300)
        title_worm.get_dir()
        title_worm.move()
        title_worm.draw(screen)
    elif state == 'game':
        screen.blit(font1.render(str(score), True, (0, 0, 0)),
                                 (15, SCREEN_SIZE[1] - 30))
        game_worm.draw(screen)
        food.draw(screen)
        if game_worm.collide(food) == 'fail':
            state = 'end'
        elif game_worm.collide(food) == 'eat':
            food = worm_obj.Food()
            game_worm.eat()
            for segment in game_worm.worm_list:
                while segment.outline.colliderect(food.outline):
                    food = worm_obj.Food()
            score += 10
            delay -= 5
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
