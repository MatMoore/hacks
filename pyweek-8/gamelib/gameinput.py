#TODO

#handle user input

import pygame
from pygame.locals import *
from constants import *

class GameInput:
    def __init__(self):
        pass
    
    def update(self, graphics, dt):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
                
        x, y = pygame.mouse.get_pos()
        self.scroll(x,y)
            
        return True

    def scroll(self):
        if x < SCROLLWIDTH:
            dx = - SCROLLSPEED*dt
        else if x > (SCREENSIZE[0]-SCROLLWIDTH):
            dx = SCROLLSPEED*dt
        if y < SCROLLWIDTH:
            dy = -SCROLLSPEED*dt
        else if y > (SCREENSIZE[1]-SCROLLWIDTH):
            dy = SCROLLSPEED*dt
        if dx or dy:
            graphics.moveCamera(dx,dy)
