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
            if unit.rect.collidepoint(location):
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
        for i in self.objects:
            i.draw(graphics)
            if i in self.units:
                self.drawHealthBar(graphics,i)

    def drawHealthBar(self,graphics,unit):
        outline = pygame.Rect(unit.rect)
        outline.top -= HEALTHBARGAP
        outline.height = HEALTHBARSIZE[1]
        outline.width = HEALTHBARSIZE[0]
        filled = pygame.Rect(outline)
        filled.width = unit.health/float(unit.maxHealth)*filled.width
        graphics.drawRect(outline, (0,255,0), 1)
        graphics.drawRect(filled, (0,255,0), 0) #TODO: adjust colour if health is low
