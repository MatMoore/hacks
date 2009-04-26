#TODO

#main game loop -
#create a world object and call its run and draw methods

#handle user input

#menus

import graphics
import gameinput
import world
from constants import *

class Game:
    def __init__(self):
        self.graphics = graphics.Graphics()
        self.gameInput = gameinput.GameInput()
        self.world = world.World()
        self.state = GAMESTATE_RUN
       
        
        
    def run(self):
        while self.state == GAMESTATE_RUN:
            if self.gameInput.update() == False:
                self.state = GAMESTATE_QUIT

            self.world.draw(self.graphics)
            self.graphics.flip()




if __name__ == '__main__':
    game = maingame()
    game.run()
