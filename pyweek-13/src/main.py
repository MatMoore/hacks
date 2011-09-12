import config
import sys
import event
import scene
import key
import level
from logging import info,debug,error
config.setupLogging()

try:
	import pygame
except ImportError:
	print 'This game requires pygame to run'
	sys.exit(1)

class GameQuit(Exception):
	pass

def pygame_init():
	'''Initialise pygame'''
	pygame.init()
	pygame.font.init()
	pygame.display.set_caption(config.get('Project','name'))

def main():
	'''Start the game'''
	info('Starting '+config.get('Project', 'name')+'...')
	pygame_init()

	clock = Clock() # Clock events drive everything
	events = event.PygameEvent(clock) # Poll pygame event queue
	events.subscribe(check_game_quit) # Listen for game quit
	controller = key.SimpleInput(events) # Map keys to meaningful input

	# Pass events through to the active scene
	director = scene.Director(clock, controller)
	director.current = level.Level('test.tmx', config.getint('Graphics','width'), config.getint('Graphics', 'height'))

	# Run
	try:
		while True:
			clock.run()
	except GameQuit:
		info('Goodbye')

class Clock(event.Publisher):
	'''Send the time since the last update to all subscribers'''
	def run(self):
		ms = pygame.time.get_ticks()
		self.publish(ms)

def check_game_quit(event_type, *args, **kwargs):
	'''Throw an exception on game quit'''
	if event_type == pygame.QUIT: raise GameQuit()
