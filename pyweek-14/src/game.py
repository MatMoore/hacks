'''Core game logic goes here'''

from resource import load_image, file_path
import pygame
from logging import info,debug,error
from config import settings
from lib.tmx import Layer, SpriteLayer, Tileset
from sprites import Camera, PlatformLayer, Player, draw_fg

class Game(object):
	'''Main game object to track anything that persists between levels'''
	def __init__(self, viewport):
		self.viewport = viewport
		object.__init__(self)

		tilesize = settings.getint('Graphics', 'tilesize')

		# Round width/height to nearest tile
		viewport = (viewport[0]/tilesize*tilesize, viewport[1]/tilesize*tilesize)
		width = viewport[0] / tilesize

		tileset = Tileset('platforms', tilesize, tilesize, 0)
		tileset.add_image(file_path('platforms.png'))
		self.platforms = PlatformLayer(width, tileset)

		self.camera = Camera(viewport)
		self.sprites = SpriteLayer()
		self.camera.layers.append(self.platforms)
		self.camera.layers.append(self.sprites)
		self.player = Player((1, -tilesize-200), self.sprites)
		self.generate_platform((0, 0), width)
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
		self.platforms.collide_wall(self.player.rect)
		self.camera.update(dt)

		for obstacle in self.platforms.collide(self.player.rect, 'platform'):
			self.player.rect.bottom = min(self.player.rect.bottom - 1, obstacle.top)
			debug('thud')
			self.player.endjump()

		self.camera.set_focus(self.player.rect.x, self.player.rect.y)

	def draw(self, screen):
		screen.fill((255, 255, 255))
		self.camera.draw(screen)
		draw_fg(screen, self.player)
		pygame.display.flip()

	def handle_pygame_event(self, event):
		self.control.handle_pygame_event(event)

	def generate_platform(self, pos, width_tiles= 1):
		i_min, j = pos
		i_max = i_min + width_tiles
		for i in range(i_min, i_max):
			debug('generating at %d %d' % (i, j))
			self.platforms[(i, j)] = self.platforms.tileset.get_tile(0)
			self.platforms[(i, j)]['platform'] = True

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
			self.player.up(dt)

	def handle_pygame_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == self.keys['up']:
				debug('boing')
				self.player.jump()

