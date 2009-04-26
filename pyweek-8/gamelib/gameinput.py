#TODO

#handle user input

import pygame
from pygame.locals import *
from constants import *

class GameInput:
    def __init__(self):
       #pygame.event.set_grab(1)
       pass
    
    def update(self, graphics, dt):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
        #TODO: make this better/neater!
        x, y = pygame.mouse.get_pos()
        dx,dy = (0,0)
        if x < SCROLLWIDTH:
            dx = - SCROLLSPEED*dt
        elif x > (SCREENSIZE[0]-SCROLLWIDTH):
            dx = SCROLLSPEED*dt
        if y < SCROLLWIDTH:
            dy = -SCROLLSPEED*dt
        elif y > (SCREENSIZE[1]-SCROLLWIDTH):
            dy = SCROLLSPEED*dt
        if dx or dy:
            graphics.moveCamera(dx,dy)
            
        return True

