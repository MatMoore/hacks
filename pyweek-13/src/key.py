from event import Publisher
import pygame
import config
from copy import copy

class SimpleInput(Publisher):
	'''Simple input device using keyboard.'''
	def __init__(self, pygame_events):
		Publisher.__init__(self)
		pygame_events.subscribe(self.process_pygame)

		self.state = {
			'up':      False,
			'down':    False,
			'left':    False,
			'right':   False,
			'action1': False,
			'action2': False,
		}

		self.keys = {}
		for key in ('up','down','left','right','action1','action2'):
			self.keys[key] = config.get('Keys', key)

	def process_pygame(self, event_type, event, *args, **kwargs):
		try:
			if event_type == pygame.KEYUP:
				action = self.keys[event.key]
				self.state[action] = False
			elif event_type == pygame.KEYDOWN:
				action = self.keys[event.key]
				self.state[action] = True
			else: return
		except KeyError:
			return

		self.publish(action, copy(self.state))
