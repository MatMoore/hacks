from constants import *
import pygame
#TODO

#Read map file to determine where initial objects go

class World:
    def __init__(self):
        self.objects = pygame.sprite.Group() #things which can be interacted with
        self.units = pygame.sprite.Group() #things which can move/die


    def select(self,rect):
        '''Try to select a group of units. Returns a list of the selected units.'''
        pass

    def addObject(self,object):
        '''Add a new object to the map'''
        self.objects.add(object)

    def addUnit(self,unit):
        '''Add a new unit to the map'''
        self.objects.add(unit)
        self.units.add(unit)

    def getUnit(self,location):
        for unit in self.units:
            if location[0] > unit.rect[0]-unit.rect[2]/2 and location[0] < unit.rect[0] + unit.rect[2]/2 \
                and location[1] > unit.rect[1]-unit.rect[3]/2 and location[1] < unit.rect[1] + unit.rect[3]/2:
                return unit

    def removeDeadUnits(self):
        '''Remove units which have been killed since the last tick'''
        for unit in self.units:
            if unit.isDead():
                unit.kill() #TODO (maybe): keep track of dead units

    def update(self,dt):
        '''Update the map. Update the objects animations and do collision detection stuff to find out which units are visible to others. Call the interact method of each unit with a list of visible objects.'''
        self.objects.update(dt)
        self.removeDeadUnits()

    def draw(self, graphics):
        '''Draw the visible part of the map onto the screen'''
        graphics.drawBackground()
        for i in self.objects.sprites():
            i.draw(graphics)
