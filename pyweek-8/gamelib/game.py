#TODO

#main game loop -
#create a world object and call its run and draw methods

#handle user input

#menus

import pygame
import graphics
import gameinput
import world
import units
import player
from constants import *

class Game:
    def __init__(self):
        self.graphics = graphics.Graphics()
        self.gameInput = gameinput.GameInput()
        self.world = world.World()
        self.state = GAMESTATE_RUN
        self.ant = units.Unit(self.graphics, (0,0),["worker1"])
        self.human = player.Player()
        self.human.addUnit(self.ant)
        self.world.addUnit(self.ant)
        
        
    def run(self):
        newtime = pygame.time.get_ticks()
        while self.state == GAMESTATE_RUN:
            oldtime = newtime
            newtime = pygame.time.get_ticks()
            dt = (newtime - oldtime)/1000.0
            if self.gameInput.update(self.graphics, dt) == False:
                self.state = GAMESTATE_QUIT
            
            self.world.update(dt)
#            self.ant.update(dt)
            self.world.draw(self.graphics)
#            self.ant.draw(self.graphics)
            self.graphics.flip()




if __name__ == '__main__':
    game = maingame()
    game.run()
