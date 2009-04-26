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
                
        #TODO: make this better/neater!
        x, y = pygame.mouse.get_pos()
        if x < SCROLLWIDTH:
            graphics.camera = (graphics.camera[0] - SCROLLSPEED*dt, graphics.camera[1])
        if x > (SCREENSIZE[0]-SCROLLWIDTH):
            graphics.camera = (graphics.camera[0] + SCROLLSPEED*dt, graphics.camera[1])
        if y < SCROLLWIDTH:
            graphics.camera = (graphics.camera[0], graphics.camera[1] -SCROLLSPEED*dt)
        if y > (SCREENSIZE[1]-SCROLLWIDTH):
            graphics.camera = (graphics.camera[0], graphics.camera[1] +SCROLLSPEED*dt)
            
        return True

