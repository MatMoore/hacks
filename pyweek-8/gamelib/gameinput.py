#TODO

#handle user input

import pygame
from pygame.locals import *
import constants

class GameInput:
    def __init__(self):
        pass
    
    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
        return True

