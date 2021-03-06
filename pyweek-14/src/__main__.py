'''Entry point for the game'''
from . import config
from .config import settings, options
from . import game
import sys
try:
	import pygame
except ImportError:
	sys.stderr.write('Please install pygame!')
	sys.exit(1)
try:
	import numpy
except ImportError:
	sys.stderr.write('Please install numpy!')
	sys.exit(1)

from logging import info, debug, error
from .game import Death, AWinnerIsYou
from .resource import load_font, load_sounds, play_music

class GameQuit(Exception):
	pass

def pygame_init(name, size):
	pygame.init()
	pygame.font.init()
	if settings.getboolean('Sound', 'enabled'):
		pygame.mixer.init()
	pygame.display.set_caption(name)
	return pygame.display.set_mode(size)

def main():
	'''Start the game'''
	config.setupLogging()

	name = settings.get('Project', 'name')
	size = settings.getint('Graphics', 'width'), \
		settings.getint('Graphics', 'height')

	info('Escape the grey goo.')

	screen = pygame_init(name, size)
	clock = pygame.time.Clock()
	load_sounds()
	play_music()

	max_framerate = settings.getint('Graphics', 'framerate')
	world = game.Game(screen.get_size(), options.level)

	try:
		while True:
			run(screen, clock, max_framerate, world)
	except GameQuit:
		info('Goodbye')

def run(screen, clock, max_framerate, world):
	'''Create a new game'''
	try:
		while True:
			ms = clock.tick(max_framerate)
			world.update(ms)
			poll(world.handle_pygame_event)
			world.draw(screen)

	except AWinnerIsYou:
		info('You win')
		c = ContinueScreen('You outlived the nanobots! Win!', (0, 100, 0))
		c.draw(screen)
		while c.waiting:
			poll(lambda x: x)

	except Death:
		info('You are dead!')
		c = ContinueScreen('You are dead! Press any key to not be dead...', (255, 0, 0))
		c.draw(screen)
		world.reset(options.level)
		while c.waiting:
			clock.tick(max_framerate)
			poll(c.handle_pygame_event)
		info('New game')

class ContinueScreen(object):
	def __init__(self, text, color):
		object.__init__(self)
		self.waiting = True
		self.text = text
		self.color = color

	def handle_pygame_event(self, event):
		if event.type == pygame.KEYDOWN:
			self.waiting = False

	def draw(self, surface):
		centred_text(self.text, surface, self.color)
		pygame.display.flip()

def centred_text(text, surface, color=(0,0,0)):
	font = load_font('VeraMono.ttf', 24)
	text = font.render(text, True, color)
	x = (surface.get_width() - text.get_width()) / 2
	y = (surface.get_height() - text.get_height()) / 2
	surface.blit(text, (x,y))


def poll(callback):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			raise GameQuit()
		callback(event)

if __name__ == '__main__':
	main()
