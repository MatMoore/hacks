import player
import units
import pygame

class AIPlayer(player.Player):
    def __init__(self, graphics, world, team=1):
        player.Player.__init__(self, graphics, world)
        self.workers = pygame.sprite.Group()
        self.fighters = pygame.sprite.Group()

    def update(self):
        if self.timerEnd == None:
            if len(self.workers.sprites()) < len(self.fighters.sprites()):
                self.buyUnit("WorkerUnit")
            else:
                self.buyUnit("SoldierUnit")
        self.getBuildStatus()
            
    
    def buyUnitReal(self):
        unit = player.Player.buyUnitReal(self)
        if unit.__class__ is units.WorkerUnit:
            self.workers.add(unit)
        else:
            self.fighters.add(unit)
        
