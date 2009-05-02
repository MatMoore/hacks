#TODO

#???

#contains units?
#groups of units
#current selected group

#resource stats
#available units ("tech level"
import pygame
import units
import math
class Player:
    def __init__(self):
        self.food = 100 #more food = more ants?
        self.usedFood = 0
        self.leaves = 100 #collect leaves to feed fungus!
        self.units = pygame.sprite.Group()
        self.colonies = pygame.sprite.Group()
        self.selectedUnits = pygame.sprite.Group()

    def buyUnit(self,type,graphics):
        unitClass = getattr(units,type)
        price = unitClass.price
        if self.food-self.usedFood > price:
            self.usedFood += price
            unit = unitClass(graphics,(0,0)) #TODO, make classes for each unit and give them their own animations
            self.units.add(unit)
            return unit

    def addColony(self,colony):
        self.colonies.add(colony)
            
    def isUnit(self, unit):
        return self.units.has(unit)
            
    def doSelect(self, location):
        self.selectedUnits.empty()
        if len(location) == 4:  #if it's a drag
        
            
            if location[2] < 0: #rect is the wrong way round horizontally(you dragged it from the right)
                location = pygame.Rect(location[0]+location[2],location[1],abs(location[2]),location[3])
            if location[3] < 0: #rect is the wrong way round vertically(you dragged it from the bottom)
                location = pygame.Rect(location[0],location[1]+location[3],location[2],abs(location[3]))
                
            for unit in self.units:                 #go through each unit
                                                    #see if it's in the rect
                if location.collidepoint(unit.position):
                    self.selectedUnits.add(unit)
        else:
            for unit in self.units:
                if unit.rect.collidepoint(location):
                    self.selectedUnits.add(unit)
                    break
    
    def doMove(self, location):
        if len(self.selectedUnits) == 1:
            self.selectedUnits.sprites()[0].walkTo(location)
        else:   #give targets seperated by the maximum radius
            #get the biggest unit
            maxRadius = 0
            for unit in self.selectedUnits:
                if unit.radius > maxRadius:
                    maxRadius = unit.radius
            
            num = math.floor(math.sqrt(len(self.selectedUnits)))
            x = location[0] - math.floor(num/2.0)*maxRadius*2
            y = location[1] - math.floor(num/2.0)*maxRadius*2
            c = 0
            for i in range(len(self.selectedUnits)):
                self.selectedUnits.sprites()[i].walkTo((x,y))
                x += maxRadius*2
                c += 1
                if c > num:
                    c = 0
                    y += maxRadius*2
                    x -= maxRadius*2*(num+1)

    def doAttack(self,enemy):
        for unit in self.selectedUnits:
            unit.attack(enemy)

    def doGather(self,resource):
        if len(self.colonies):
            colony = self.colonies.sprites()[0]
            for unit in self.selectedUnits:
                unit.gather(resource,colony)
            
    def drawSelectedRects(self, graphics):
        for unit in self.selectedUnits:
            rect = (unit.position[0]-unit.radius,unit.position[1]-unit.radius,unit.radius*2, unit.radius*2)
            graphics.drawRect(rect, (255,0,0), 1)
