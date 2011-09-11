import config
import sys
from logging import info,debug,error
config.setupLogging()

try:
	import pygame
except ImportError:
	print 'This game requires pygame to run'
	sys.exit(1)

def pygame_init():
	pass

def main():
	info('Starting '+config.get('Project', 'name')+'...')
	pygame_init()
	game = Controller()
	while game.tick():
		pass
	info('Goodbye')

class Controller(object):
	def __init__(self):
		pass

	def tick(self):
		return False
