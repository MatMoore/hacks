import player
import units
import pygame
import math
import stuff
import random
from constants import *

class AIPlayer(player.Player):
    def __init__(self, graphics, world, team=1):
        player.Player.__init__(self, graphics, world, team)
        self.workers = pygame.sprite.Group()
        self.fighters = pygame.sprite.Group()
        self.timer = stuff.Timer(10000) #stuff to do each second
        
    def findCloseGrass(self):
        bestItem = None
        bestDistance = MAXAIDISTANCE**2
        colonypos = self.colonies.sprites()[0].rect.center
        for item in self.world.resources:
            itempos = item.rect.center
            distance = (itempos[0] - colonypos[0])**2 + (itempos[1] - colonypos[1])**2
            if distance < bestDistance:
                bestItem = item
                bestDistance = distance
        return bestItem
        
    def update(self):
        if self.timer.ready():
            if self.timerEnd == None:
                if (len(self.workers.sprites())*3 < len(self.fighters.sprites()) or len(self.workers.sprites()) < 2) and (len(self.workers.sprites()) + len(self.fighters.sprites()) < 30):
                    self.buyUnit("WorkerUnit")
                else:
                    self.buyUnit("SoldierUnit")
            self.getBuildStatus()
        
            self.bestGrass = self.findCloseGrass()
            for unit in self.workers:
                if len(unit.targets) == 0:
                    unit.gather(self.bestGrass, self.colonies.sprites()[0])
            
            for unit in self.fighters:
                if len(unit.targets) == 0:
                    target = random.choice(self.world.units.sprites())
                    if target not in self.workers and target not in self.fighters:
                        unit.attack(target)
    
    def buyUnitReal(self):
        unit = player.Player.buyUnitReal(self)
        if unit.__class__ is units.WorkerUnit:
            self.workers.add(unit)
        else:
            self.fighters.add(unit)
        
