#TODO

#main game loop -
#create a world object and call its run and draw methods

#handle user input

#menus

import pygame
from pygame.locals import *
import graphics
import world
import player
from constants import *

class Game:
    def __init__(self):
        self.graphics = graphics.Graphics()
        self.world = world.World()
        self.state = GAMESTATE_RUN
        self.human = player.Player()
        unit = self.human.buyUnit("Unit",self.graphics)
        if unit:
            self.world.addUnit(unit)
        
    def doInputEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
        return True
    
    def doScroll(self, dt):
        x, y = pygame.mouse.get_pos()
        dx,dy = (0,0)
        if x < SCROLLWIDTH:
            dx = - SCROLLSPEED*dt
        elif x > (SCREENSIZE[0]-SCROLLWIDTH):
            dx = SCROLLSPEED*dt
        if y < SCROLLWIDTH:
            dy = -SCROLLSPEED*dt
        elif y > (SCREENSIZE[1]-SCROLLWIDTH):
            dy = SCROLLSPEED*dt
        if dx or dy:
            self.graphics.moveCamera(dx,dy)

        
    def run(self):
        newtime = pygame.time.get_ticks()
        while self.state == GAMESTATE_RUN:
            oldtime = newtime
            newtime = pygame.time.get_ticks()
            dt = (newtime - oldtime)/1000.0

            self.doScroll(dt)
            
            if self.doInputEvents() == False:
                self.state = GAMESTATE_QUIT
                            
            self.world.update(dt)
            self.world.draw(self.graphics)
            self.graphics.flip()




if __name__ == '__main__':
    game = maingame()
    game.run()
