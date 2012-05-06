'''Core game logic goes here'''

from logging import info,debug,error

class Game(object):
	'''Main game object to track anything that persists between levels'''
	def __init__(self, screen):
		self.screen = screen
		object.__init__(self)

	def update(self, dt):
		debug(dt)

	def handle_pygame_event(self, event):
		pass
