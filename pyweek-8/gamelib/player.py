#TODO

#???

#contains units?
#groups of units
#current selected group

#resource stats
#available units ("tech level"
import pygame
class Player:
    def __init__(self):
        self.food = 100 #more food = more ants?
        self.leaves = 100 #collect leaves to feed fungus!
        self.units = pygame.sprite.Group()

    def addUnit(self,unit):
        self.units.add(unit)
