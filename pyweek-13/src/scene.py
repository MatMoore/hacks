import config
import pygame
import resource
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

class StartScene(object):
	def __init__(self, director, next_screen):
		object.__init__(self)
		self.director = director
		self.next_screen = next_screen
		self.image = resource.load_image('woman-holding-drawing.png')

	def draw(self, screen):
		screen.blit(self.image, (0,0))
		pygame.display.flip()

	def input_changed(self, *args):
		self.director.current=self.next_screen

class EndScene(object):
	def __init__(self, director):
		object.__init__(self)
		self.director = director
		self.image = resource.load_image('jacques-fosse.png')
		pygame.display.flip()

	def draw(self, screen):
		screen.blit(self.image, (0,0))
		pygame.display.flip()
