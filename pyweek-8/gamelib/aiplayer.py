import player
import units
import pygame
import math
import stuff
import random
import mapobject
from constants import *

class AIPlayer(player.Player):
    def __init__(self, graphics, world, team=2):
        player.Player.__init__(self, graphics, world, team)
        self.workers = pygame.sprite.Group()
        self.fighters = pygame.sprite.Group()
        
        self.timer = stuff.Timer(5000) #stuff to do each second
        
    def findCloseGrass(self):
        bestItem = None        
        
        bestDistance = MAXAIDISTANCE**2
        if self.colonies.sprites():
            colonypos = self.colonies.sprites()[0].rect.center
        else:
            return None
            
        for item in self.world.resources:
            itempos = item.rect.center
            distance = (itempos[0] - colonypos[0])**2 + (itempos[1] - colonypos[1])**2
            if distance < bestDistance:
                bestItem = item
                bestDistance = distance
        return bestItem
        
    def update(self):
        if self.timer.ready():
            if self.colonies.sprites():
                if self.colonies.sprites()[0].attackingUnit:
                    for units in self.fighters:
                        units.attack(self.colonies.sprites()[0].attackingUnit)
                    
            if self.timerEnd == None:
                if (len(self.workers.sprites())*3 < len(self.fighters.sprites()) or len(self.workers.sprites()) < 2) and (len(self.workers.sprites()) + len(self.fighters.sprites()) < 30):
                    self.buyUnit("WorkerUnit")
                else:
                    self.buyUnit("SoldierUnit")
            
            self.getBuildStatus()
            
            self.bestGrass = self.findCloseGrass()
            if self.bestGrass:
                for unit in self.workers:
                    if len(unit.targets) == 0 and self.colonies.sprites():
                        unit.gather(self.bestGrass, self.colonies.sprites()[0])
            
            for unit in self.fighters:
                if len(unit.targets) == 0:
                    for i in range(5):  #give 5 chances to grab an enemy
                        target = random.choice(self.world.units.sprites())
                        if target not in self.workers and target not in self.fighters:
                            unit.attack(target)
                            break
                if unit.health < 30 and self.colonies.sprites():    #come home if low health
                    unit.walkTo((self.colonies.sprites()[0].rect.centerx + random.randint(-1000,1000), self.colonies.sprites()[0].rect.centery + random.randint(-1000,1000)))
            
            #1 in 100 chance of attacking colony
            if random.randint(0,100) == 500 or (len(self.workers.sprites()) + len(self.fighters.sprites()) == len(self.world.units.sprites())):
                for thing in self.world.bg:
                    if thing.__class__ == mapobject.Colony:
                        if self.colonies.sprites():
                            if self.colonies.sprites()[0] != thing:
                                for unit in self.fighters:
                                    unit.attack(thing)
                    
    
    def buyUnitReal(self):
        unit = player.Player.buyUnitReal(self)
        if unit:
            if unit.__class__ is units.WorkerUnit:
                self.workers.add(unit)
            else:
                self.fighters.add(unit)
        
