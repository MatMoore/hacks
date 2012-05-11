'''Entry point for the game'''
import config
from config import settings
import game
import pygame
from logging import info, debug, error
from game import Death, AWinnerIsYou

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
	max_framerate = settings.getint('Graphics', 'framerate')

	done = False
	while not done:
		world = game.Game(screen.get_size())
		try:
			while True:
				ms = clock.tick(max_framerate)
				world.update(ms)
				poll(world.handle_pygame_event)
				world.draw(screen)
		except GameQuit:
			info('Goodbye')
			done = True
		except AWinnerIsYou:
			info('You win')
			# TODO continue screen
		except Death:
			info('You are dead!')
			# TODO continue screen

def poll(callback):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			raise GameQuit()
		callback(event)
