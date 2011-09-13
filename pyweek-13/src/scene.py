import config
import pygame
from logging import info,debug,error

class Director(object):
	'''Control the currently visible scene'''
	def __init__(self, clock, controller):
		self.current = None
		clock.subscribe(self.tick)
		controller.subscribe(self.input_changed)
		self.set_screen((config.getint('Graphics','width'), config.getint('Graphics', 'height')))

	def set_screen(self, size):
		'''Set the screen mode'''
		self.screen = pygame.display.set_mode(size)

	def tick(self, ms):
		'''Update the scene and draw it'''
		self.direct('tick', ms)
		self.direct('draw', self.screen)

	def input_changed(self, *args, **kwargs):
		self.direct('input_changed', *args, **kwargs)

	def direct(self, f_name, *args, **kwargs):
		'''Do stuff with the current scene'''
		if self.current:
			try:
				f = getattr(self.current, f_name)
			except AttributeError:
				return
			f(*args, **kwargs)
