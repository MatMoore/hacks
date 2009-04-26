from constants import *
#TODO

#Read map file to determine where initial objects go

class World:
    def __init__(self, graphics):
        self.objects = [] #things which can be interacted with
        self.units = [] #things which can move/die


    def select(self,rect):
        '''Try to select a group of units. Returns a list of the selected units.'''
        pass

    def addObject(self,object):
        '''Add a new object to the map'''
        self.objects.append(object)

    def addUnit(self,unit):
        '''Add a new unit to the map'''
        self.objects.append(unit)
        self.units.append(unit)

    def removeDeadUnits(self):
        '''Remove units which have been killed since the last tick'''
        pass

    def run(self):
        '''Do collision detection stuff to find out which units are visible to others. Call the interact method of each unit with a list of visible objects.'''
        pass

    def draw(self, graphics):
        '''Draw the visible part of the map onto the screen'''
        graphics.drawBackground()
        
        pass
