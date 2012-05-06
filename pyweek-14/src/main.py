'''Entry point for the game'''
import config
from config import settings
import game
import pygame
from logging import info, debug, error
from control import Controller,GameQuit


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

	info('Starting '+name+'...')

	screen = pygame_init(name, size)

	# create models
	world = game.Game(screen)

	# create controllers
	controller = Controller()
	controller.ticks.add_listener(world.update)
	controller.events.add_listener(world.handle_pygame_event)

	# run game
	try:
		while True:
			controller.tick()
	except GameQuit:
		info('Goodbye')
