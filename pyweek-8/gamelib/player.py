#TODO

#???

#contains units?
#groups of units
#current selected group

#resource stats
#available units ("tech level"
import pygame
import units
class Player:
    def __init__(self):
        self.food = 100 #more food = more ants?
        self.usedFood = 0
        self.leaves = 100 #collect leaves to feed fungus!
        self.units = pygame.sprite.Group()
        self.selectedUnits = pygame.sprite.Group()

    def buyUnit(self,type,graphics):
        unitClass = getattr(units,type)
        price = unitClass.price
        if self.food-self.usedFood > price:
            self.usedFood += price
            unit = unitClass(graphics,(0,0)) #TODO, make classes for each unit and give them their own animations
            self.units.add(unit)
            return unit
            
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
        for unit in self.selectedUnits:
            unit.walkTo(location)

    def doAttack(self,enemy):
        for unit in self.selectedUnits:
            unit.attack(enemy)
            
    def drawSelectedRects(self, graphics):
        for unit in self.selectedUnits:
            graphics.drawRect(unit.rect, (255,0,0), 1)
