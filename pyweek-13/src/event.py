'''Stuff for handling events'''
import pygame

class Publisher(object):
	'''Publish arbitary data to whichever objects have registered event handlers'''
	def __init__(self):
		self.handlers = set()

	def subscribe(self, handler):
		self.handlers.add(handler)

	def unsubscribe(self, handler):
		self.handlers.remove(handler)

	def publish(self, *args, **kwargs):
		for handler in self.handlers:
			handler(*args, **kwargs)

class PygameEvent(Publisher):
	'''Poll the pygame event queue and publish events'''
	def __init__(self, clock):
		Publisher.__init__(self)
		clock.subscribe(self.poll)

	def poll(self, *args, **kwargs):
		for event in pygame.event.get():
			self.publish(event.type, event)
