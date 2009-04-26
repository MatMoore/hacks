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

    def buyUnit(self,type,graphics):
        unitClass = getattr(units,type)
        price = unitClass.price
        if self.food-self.usedFood > price:
            self.usedFood += price
            unit = unitClass(graphics,(0,0),["worker1"]) #TODO, make classes for each unit and give them their own animations
            self.units.add(unit)
            return unit
            
    def doSelect(self, location, button):
        if location.__class__ == pygame.rect.Rect:  #if it's a drag
            #do drag stuff
            pass
        else:
            #it was a click
            pass
