import config
config.setupLogging()
import sys
import event
import scene
import key
import level
from logging import info,debug,error
from util import throttle

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
	#events.subscribe(log_mouse_pos)
	controller = key.SimpleInput(events) # Map keys to meaningful input

	# Pass events through to the active scene
	director = scene.Director(clock, controller)
	director.current = level.Level('level1.tmx', config.getint('Graphics','width'), config.getint('Graphics', 'height'))

	pauseScreen = PauseScreen(director)
	events.subscribe(pauseScreen.pause)

	# Run
	try:
		while True:
			clock.run()
			#while True:pass
	except GameQuit:
		info('Goodbye')

class Clock(event.Publisher):
	'''Send the time since the last update to all subscribers'''
	def __init__(self):
		event.Publisher.__init__(self)
		self.source = pygame.time.Clock()

	def run(self):
		ms = self.source.tick()
		self.publish(ms)
		self.log_fps()

	@throttle(50)
	def log_fps(self):
		fps = self.source.get_fps()
		if fps < 100:
			debug('fps: %s', fps)

def check_game_quit(event_type, *args, **kwargs):
	'''Throw an exception on game quit'''
	if event_type == pygame.QUIT: raise GameQuit()

def log_mouse_pos(event_type, event, *args, **kwargs):
	'''Log mouse position'''
	if event_type == pygame.MOUSEMOTION:
		debug(event.pos)

class PauseScreen(object):
	def __init__(self, director):
		self.paused = False
		self.prev = None
		self.director = director
	
	def pause(self, event_type, event, *args, **kwargs):
		'''Pause game'''
		if event_type == pygame.MOUSEBUTTONDOWN:
			if self.paused:
				info('Unpaused')
				self.director.current = self.prev
			else:
				info('Paused')
				self.prev = self.director.current
				self.director.current = self
				try:
					self.prev.debug()
				except: pass
			self.paused = not self.paused

