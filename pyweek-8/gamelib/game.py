#TODO

#main game loop -
#create a world object and call its run and draw methods

#handle user input

#menus

import graphics
import gameinput
from constants import *

class Game:
    def __init__(self):
        self.graphics = graphics.Graphics()
        self.gameinput = gameinput.GameInput()
        self.state = GAMESTATE_RUN
        
    def run(self):
        while self.state == GAMESTATE_RUN:
            if self.gameinput.update() == False:
                self.state = GAMESTATE_QUIT

            self.graphics.drawBackground(BACKGROUNDIMAGE)
            self.graphics.flip()




if __name__ == '__main__':
    game = maingame()
    game.run()
