'''Simple event manager using the observer pattern. This decouples models/views/controllers.'''

class EventManager(object):
	def __init__(self):
		self.listeners = []

	def add_listener(self, listener):
		'''Register a callback function to be called with every new event'''
		self.listeners.append(listener)
	
	def remove_listener(self, listener):
		'''Unregister the callback function'''
		self.listeners.remove(listener)

	def post(self, *args):
		'''Post an event to all listeners'''
		for listener in self.listeners:
			listener(*args)
