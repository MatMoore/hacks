'''Core game logic goes here'''

from resource import load_image, file_path
import pygame
from logging import info,debug,error
from config import settings
from lib.tmx import Layer, SpriteLayer
from sprites import Camera, PlatformLayer, Player

class Game(object):
	'''Main game object to track anything that persists between levels'''
	def __init__(self, viewport):
		self.viewport = viewport
		object.__init__(self)

		self.camera = Camera(viewport)
		self.sprites = SpriteLayer()
		self.platforms = PlatformLayer()
		self.camera.layers.append(self.platforms)
		self.camera.layers.append(self.sprites)
		self.player = Player((0, 0), self.sprites)
		self.generate_platform((-1, -1))
		self.control = PlayerInput(self.player)

	def update(self, dt):
		# remove everything that has gone past the bottom of the screen
		# apply gravity to player
		# apply player movement
		# handle player - platform/wall collisions
		# handle player - goo collisions
		# if sand on screen and > next platform time:
		#   generate platform
		#   generate next platform time
		self.control.update(dt)
		self.camera.set_focus(self.player.rect.x, self.player.rect.y)
		self.camera.update(dt)

	def draw(self, screen):
		screen.fill((255, 255, 255))
		self.camera.draw(screen)
		pygame.display.flip()

	def handle_pygame_event(self, event):
		pass

	def generate_platform(self, pos, width_tiles= 1):
		i_min, j = pos
		i_max = i_min + width_tiles
		for i in range(i_min, i_max):
			debug('generating at %d %d' % (i, j))
			self.platforms[(i, j)] = self.platforms.tileset.get_tile(0)

class PlayerInput(object):
	def __init__(self, player):
		self.player = player

		self.keys = {}
		for action in ('left', 'right', 'up', 'down'):
			value = settings.getint('Controls', action)
			self.keys[action] = value
			debug('Setting %s to %s' % (action, value))

	def update(self, dt):
		keys = pygame.key.get_pressed()
		if keys[self.keys['left']]:
			self.player.left(dt)
		elif keys[self.keys['right']]:
			self.player.right(dt)
		if keys[self.keys['up']]:
			self.player.rect.top -= self.player.speed * dt
		elif keys[self.keys['down']]:
			self.player.rect.top += self.player.speed * dt

