import pygame
from pygame.locals import *

class MapObject(pygame.sprite.Sprite):
    '''Base class for all objects that are part of a map'''
    def __init__(self,surface,position):
        '''Surface = image to use, position = top left coordinates'''
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.rect = pygame.Rect(position,surface.get_size())

    def draw(self,graphics):
        '''Draw the object if it is visible'''
        graphics.drawImage(self.surface, self.rect, angle=0)
