from constants import *
import pygame
import math
import units
import mapobject
import random

#TODO

#Read map file to determine where initial objects go

class World:
    def __init__(self):
        self.objects = pygame.sprite.Group() #everything
        self.bg = pygame.sprite.Group() #background objects
        self.fg = pygame.sprite.Group() #objects that can be bumped into?
        self.units = pygame.sprite.Group() #things which can move/die
        self.resources = pygame.sprite.Group() #things which can be collected

    def select(self,rect):
        '''Try to select a group of units. Returns a list of the selected units.'''
        pass

    def addObject(self,object,ghost=True):
        '''Add a new object to the map'''
        if ghost:
            self.bg.add(object)
        else:
            self.fg.add(object) #can bump into it
        self.objects.add(object)

    def addUnit(self,unit):
        '''Add a new unit to the map'''
        self.objects.add(unit)
        self.units.add(unit)

    def addResource(self,unit):
        '''Add a new resource to the map'''
        self.objects.add(unit)
        self.bg.add(unit)
        self.resources.add(unit)

    def getUnit(self,location):
        for unit in self.units:
            if unit.rect.collidepoint(location):
                return unit

    def getResource(self,location):
        for unit in self.resources:
            if unit.rect.collidepoint(location):
                return unit

    def getColony(self,location):
        for unit in self.bg:
            if unit.__class__ is mapobject.Colony:
                if unit.rect.collidepoint(location):
                    return unit


    def removeDeadUnits(self):
        '''Remove units which have been killed since the last tick'''
        for unit in self.units:
            if unit.isDead():
                unit.kill() #TODO (maybe): keep track of dead units
                
        for unit in self.bg:
            try:
                if unit.isDead():
                    unit.kill   #kill the colony
            except:
                pass
                    
    def addLeaves(self, graphics):
        for i in range(NUMBEROFLEAVES):
            regen = True
            while regen:
                regen = False
                randomPos = (random.randint(-MAXAIDISTANCE,MAXAIDISTANCE), random.randint(-MAXAIDISTANCE,MAXAIDISTANCE))
                for bgobj in self.bg:
                    pos = bgobj.rect.center
                    if math.sqrt(  (pos[0]-randomPos[0])**2 + (pos[1]-randomPos[1])**2  ) < bgobj.radius + bgobj.radius + SEPERATION:
                        regen = True
                        break   #break out of for loop to gen a new random position
                        
            self.addResource(mapobject.Leaves(randomPos,graphics))

    def update(self,dt):
        '''Update the map. Update the objects animations and do collision detection stuff to find out which units are visible to others. Call the interact method of each unit with a list of visible objects.'''
        self.objects.update(dt)
        self.removeDeadUnits()
        grid = dict()
        
        #first pass: put each object into grid
        for obj in self.objects:
#            gridX = int(math.floor(obj.position[0] / GRIDSIZE))
#            gridY = int(math.floor(obj.position[1] / GRIDSIZE))
            if self.bg.has(obj): #ignore the background
                continue
            gridX = obj.rect.centerx / GRIDSIZE #only units have position, but all sprites have a rect + we don't need the accuracy here
            gridY = obj.rect.centery / GRIDSIZE

            if (gridX,gridY) not in grid:
                grid[(gridX,gridY)] = pygame.sprite.Group()

            grid[(gridX,gridY)].add(obj)
        
        #second pass - go through dictionary
        for key in grid.keys():
            localObjects = pygame.sprite.Group()
            for x in range(key[0]-1, key[0]+2):
                for y in range(key[1]-1, key[1]+2):
                    if (x,y) in grid:
                        for obj in grid[(x,y)]:
                            localObjects.add(obj)
            
            for obj in grid[key]:
                try:                            #because the object might not implement interact, we check if it exists by
                    getattr(obj, "interact")    #attempting to get the attributes
                except AttributeError:
                    pass
                else:
                    obj.interact(localObjects)
                            

                

    def draw(self, graphics):
        '''Draw the visible part of the map onto the screen'''
        graphics.drawBackground()
        
        for i in self.bg:    #draw resources/background objects first
            i.draw(graphics)

        for i in self.fg: #draw other objects
            i.draw(graphics)

        for i in self.units:        #then units
            i.draw(graphics)
            self.drawHealthBar(graphics,i)

        for i in self.units:    #doing this afterwards so that lasers are on top of stuff
            if i.__class__ is units.SoldierUnit:
                if i.laser and i.attackTarget.sprites():
                    graphics.drawLine(i.position, i.attackTarget.sprites()[0].position)


    def drawHealthBar(self,graphics,unit):
        outline = pygame.Rect(unit.position[0]-unit.radius,unit.position[1]-unit.radius,unit.radius*2, unit.radius*2)
        outline.top -= HEALTHBARGAP
        outline.height = HEALTHBARSIZE[1]
        outline.width = HEALTHBARSIZE[0]
        filled = pygame.Rect(outline)
        filled.width = unit.health/float(unit.maxHealth)*filled.width
        graphics.drawRect(outline, (0,255,0), 1)
        graphics.drawRect(filled, (0,255,0), 0) #TODO: adjust colour if health is low
