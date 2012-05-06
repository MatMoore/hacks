'''Generate events based on the pygame clock'''

import pygame
from config import settings
from event import EventManager

class GameQuit(Exception):
	pass

class Controller(object):
	'''Generates events every tick and polls the pygame event queue'''

	def __init__(self):
		self.ticks = EventManager()
		self.events = EventManager()
		self._clock = pygame.time.Clock()
		self.max_framerate = settings.getint('Graphics', 'framerate')

	def tick(self):
		'''Check the pygame clock and generate an event'''
		ms = self._clock.tick(self.max_framerate)
		self.ticks.post(ms)
		self._poll()

	def _poll(self):
		'''Poll the pygame event queue and publish events'''
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				raise GameQuit()
			self.events.post(event)
