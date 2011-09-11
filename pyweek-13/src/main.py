import config
from logging import info,debug,error
config.setupLogging()

def main():
	info('Starting '+config.get('Project', 'name')+'...')
	game = Controller()
	while game.tick():
		pass
	info('Goodbye')

class Controller(object):
	def __init__(self):
		pass

	def tick(self):
		return False
