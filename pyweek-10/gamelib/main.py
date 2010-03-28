'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import data, game, constants

def main():

	gameInstance = game.Game()
	gameState = constants.gsInGame

	while gameState != constants.gsQuit:
		if gameState == constants.gsInGame:
			gameState = gameInstance.main()
