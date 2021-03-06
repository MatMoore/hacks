import pygame
from pygame.locals import *

class MapObject(pygame.sprite.Sprite):
    '''Base class for all objects that are part of a map'''
    def __init__(self,surface,position,team=None):
        '''Surface = image to use, position = top left coordinates'''
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.rect = pygame.Rect(surface.get_rect())
        self.rect.center = position
        self.direction = 270
        self.radius = max(surface.get_size())/2 #default radius = maximum of the surface sizes divided by 2
        self.team = team
        self.health = 100   #ok i've put this here, along with isDead() because maybe it'll be better
        
    def draw(self,graphics):
        '''Override draw method so that we can use world coordinates instead of camera ones'''
        
        self.rect = graphics.drawImage(self.surface, self.rect, round(self.direction))
        #we update the self.rect because the angle will change the rectangle shape

    def isDead(self):
        return self.health <= 0       

class Leaves(MapObject):
    '''Resource for the worker ants to collect'''

    imageName = 'pileofleaves.png'
    def __init__(self,position,graphics):
        surface = graphics.loadImage(Leaves.imageName)
        MapObject.__init__(self,surface,position)
        self.amount = 100

    def take(self):
        self.amount -= 1

class Colony(MapObject):
    imageName = 'mound.png'
    def __init__(self,player,position,graphics,team=1):
        surface = graphics.loadImage(Colony.imageName)
        self.player = player
        MapObject.__init__(self,surface,position,team)
        self.position = self.rect.center    #since this is destructable and things rely on position, we add it here
        self.health = 1000
        self.attackingUnit = None
        
    def addLeaves(self,amount):
        self.player.leaves += amount



    def bitten(self, power, unit):
        self.attackingUnit = unit
        self.health -= power
