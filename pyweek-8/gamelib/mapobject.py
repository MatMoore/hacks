import pygame
from pygame.locals import *

class MapObject(pygame.sprite.Sprite):
    '''Base class for all objects that are part of a map'''
    def __init__(self,surface,position):
        '''Surface = image to use, position = top left coordinates'''
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.rect = pygame.Rect(position,surface.get_size())
        self.direction = 0

    def draw(self,graphics):
        '''Override draw method so that we can use world coordinates instead of camera ones'''
        
        self.rect = graphics.drawImage(self.surface, self.rect, round(self.direction))
        #we update the self.rect because the angle will change the rectangle shape
