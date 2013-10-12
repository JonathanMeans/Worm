# Objects for Worm game
import pygame
from worm_fun import *
import random
from pygame.locals import *
import math

SCREEN_SIZE = (300, 300)

#color variables
BLACK = 0,0,0
WGREEN = 0,255,100


class Segment:
    """A 'block' that forms part of the Worm's body."""
    
    def __init__(self, x, y):
        """Initialize the Segement.

        Keyword arguments:
        x -- the left edge of the Segment
        y -- the top edge of the Segment

        """
        
        self.x = x
        self.y = y
        #self.box is a red square, self.outline is a thin black border
        self.box = pygame.Rect(x+1, y+1, 8, 8)
        self.outline = pygame.Rect(x, y, 10, 10)

    def draw(self, surf):
        self.surf = surf
        pygame.draw.rect(surf, BLACK, self.outline)
        pygame.draw.rect(surf, WGREEN, self.box)
        
class Food:
    """Create a randomly-placed block of food."""
    
    def __init__(self):
        self.x = random.randint(0, (SCREEN_SIZE[0] - 10)/10) * 10
        self.y = random.randint(0, (SCREEN_SIZE[1] - 10)/10) * 10
        self.outline = pygame.Rect(self.x, self.y, 10, 10)
    def draw(self, surf):
        self.surf = surf
        pygame.draw.rect(surf, (128, 0, 128), self.outline)

class Worm:
    def __init__(self):
        #Create a worm of length 6
        self.worm_list = []
        x = random.randint(6, SCREEN_SIZE[0]/10) * 10
        y = random.randint(0, SCREEN_SIZE[1]/10) * 10
        self.direction = 'right'
        self.worm_list.append(Segment(x, y))
        for pair in [(x-10,y),(x-20,y),(x-30,y),(x-40,y),(x-50,y)]:
            self.worm_list.append(Segment(pair[0], pair[1]))
        
    def draw(self, surf):
        for segment in self.worm_list:
            segment.draw(surf)

    def move(self, food):
        head = self.worm_list[0]
        self.worm_list.pop()
        
        #Append new segment in direction of motion
        if self.direction == 'up':
            self.worm_list.insert(0, Segment(head.x, head.y - 10))
        elif self.direction == 'down':
            self.worm_list.insert(0, Segment(head.x, head.y + 10))
        elif self.direction == 'left':
            self.worm_list.insert(0, Segment(head.x - 10, head.y))
        elif self.direction == 'right':
            self.worm_list.insert(0, Segment(head.x + 10, head.y))

    def change_dir(self, food):
        pressed_keys = pygame.key.get_pressed()
        # != bit is there to prevent Worm from going straight backwards.
        # Do not replace with, e.g. if self.direction == 'up'.
        # This will break with rapid inputs.
        if pressed_keys[K_DOWN]:
            if self.worm_list[0].x != self.worm_list[1].x:
                self.direction = 'down'
        if pressed_keys[K_UP]:
            if self.worm_list[0].x != self.worm_list[1].x:
                self.direction = 'up'
        if pressed_keys[K_RIGHT]:
            if self.worm_list[0].y != self.worm_list[1].y:
                self.direction = 'right'
        if pressed_keys[K_LEFT]:
            if self.worm_list[0].y != self.worm_list[1].y:
                self.direction = 'left'

    def collide(self, food):
        head = self.worm_list[0]
        # Return 'fail' if worm goes outside bounds
        if head.x <0 or head.y <0 or head.x + 10 > SCREEN_SIZE[0]:
            return 'fail'
        if head.y + 10 > SCREEN_SIZE[1]:
            return 'fail'
        # Return 'fail' if worm touches itself.
        for segment in self.worm_list[1:]:
            if head.outline.colliderect(segment.outline):
                return 'fail'
        # Note if worm eats food
        if head.outline.colliderect(food.outline):
            return 'eat'
        return 'clear'

    def eat(self):
        # Inserts a head head in front of worm, making it grow.
        # movement not jerky
        head = self.worm_list[0]
        tail = self.worm_list[-1]
        pretail = self.worm_list[-2]
        if pretail.x == tail.x:
            assert pretail.y != tail.y
            if pretail.y > tail.y:
                x = tail.x
                y = tail.y - 10
            elif pretail.y < tail.y:
                x = tail.x
                y = tail.y + 10
        else:
            assert pretail.y == tail.y
            if pretail.x < tail.x:
                x = tail.x + 10
                y = tail.y
            elif pretail.x > tail.x:
                x = tail.x - 10
                y = tail.y
        new_head = Segment(x, y)
        self.worm_list.append(new_head)

class TitleWorm(Worm):
    #This is a subclass of the playable worm. It just rotates around
    #the main text.
    def __init__(self):
        self.worm_list = []
        self.direction = 'right'
        for pair in [(200, 150), (190, 150), (180, 150),
                     (170, 150), (160, 150), (150, 150), (140, 150)]:
            self.worm_list.append(Segment(pair[0], pair[1]))

    def get_dir(self):
        head = self.worm_list[0]
        x = head.x
        y = head.y
        print x,y
        if x > 240 and y > 140:
            self.direction = 'up'
        elif x < 120 and y <= 100:
            self.direction = 'down'
        elif y < 100:
            self.direction = 'left'
        elif y > 140:
            self.direction = 'right'

class SmartWorm(Worm):
    def move(self, food):
        self.food = food
        head = self.worm_list[0]
        self.get_dir(food, head)
        self.worm_list.pop()

        #Append new segment in direction of motion
        if self.direction == 'up':
            self.worm_list.insert(0, Segment(head.x, head.y - 10))
        elif self.direction == 'down':
            self.worm_list.insert(0, Segment(head.x, head.y + 10))
        elif self.direction == 'left':
            self.worm_list.insert(0, Segment(head.x - 10, head.y))
        elif self.direction == 'right':
            self.worm_list.insert(0, Segment(head.x + 10, head.y))

    def get_dir(self, food, head):
        self.food = food
        self.head = head
        weights = {}
        adjacent = get_adjacent(self.head.x, self.head.y)
        for square in adjacent:
            weights[square] = distance(square[0], square[1], food)
            for segment in self.worm_list:
                weights[square] -= distance(square[0], square[1], segment)/(len(self.worm_list)/1.15)
                if square[0] == segment.x and square[1] == segment.y:
                    weights[square] = 1000000
            if square[0] < 0 or square[0] >= SCREEN_SIZE[0] or square[1] < 0 or square[1] >= SCREEN_SIZE[1]:
                weights[square] = 1000000
        sq, nxt = 0, 10000000000
        for weight in weights.keys():
            if weights[weight] < nxt:
                nxt = weights[weight]
                sq = weight
        self.direction = direction(sq[0],sq[1], self.head)
                                
