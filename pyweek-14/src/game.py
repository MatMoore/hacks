'''Core game logic goes here'''

from resource import load_image, file_path
import pygame
from logging import info,debug,error
from config import settings
from lib.tmx import Layer, SpriteLayer, Tileset
from sprites import Camera, PlatformLayer, Player, draw_fg, GooLayer

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
		self.goo = GooLayer()
		self.camera.layers.append(self.platforms)
		self.camera.layers.append(self.sprites)
		self.camera.layers.append(self.goo)
		self.player = Player((1, -tilesize), self.sprites)
		self.generate_platform((0, 0), 15)
		self.generate_platform((0, -20), 15)
		self.control = PlayerInput(self.player)
		self.next_platform = -viewport[1]-10

	def update(self, dt):
		# remove everything that has gone past the bottom of the screen
		# apply gravity to player
		# apply player movement
		# handle player - platform/wall collisions
		# handle player - goo collisions
		# if sand on screen and > next platform time:
		#   generate platform
		#   generate next platform time
		height_before = self.player.rect.bottom

		# Handle input
		self.control.update(dt)
		self.platforms.collide_wall(self.player.rect)

		# Update platform layer, goo layer, and sprite positions
		self.camera.update(dt)

		# Player can only collide with stuff from above.
		# It might be a bit glitchy if the player falls into a platform from the side,
		# but lets just let that slide
		resting = False
		for obstacle in self.platforms.collide(self.player.rect, 'platform'):
			if height_before <= obstacle.top:
				self.player.rect.bottom = min(self.player.rect.bottom, obstacle.top)
				debug('thud')
				self.player.endjump()
			resting = True
		if not resting:
			debug('uh oh')
			self.player.resting = False

		self.camera.set_focus(self.player.rect.x, self.player.rect.y)

		if self.goo.level <= self.player.rect.bottom:
			info('You are dead')
			return

		# Remove old platforms
		self.platforms.remove_assimilated(self.goo.level)

		# Generate out of view platforms
		if self.camera.viewport.top <= self.next_platform:
			y = self.next_platform/self.platforms.tile_height
			self.generate_platform((0,y-1), 5)
			self.next_platform -= 300

	def draw(self, screen):
		screen.fill((255, 255, 255))
		self.camera.draw(screen)
		draw_fg(screen, self.player)
		pygame.display.flip()

	def handle_pygame_event(self, event):
		self.control.handle_pygame_event(event)

	def generate_platform(self, pos, width_tiles = 1):
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
		self.jumping = False

	def update(self, dt):
		keys = pygame.key.get_pressed()
		if keys[self.keys['left']]:
			self.player.left(dt)
		elif keys[self.keys['right']]:
			self.player.right(dt)
		if self.jumping:
			self.player.jump()
		if keys[self.keys['up']]:
			self.player.up(dt)

	def handle_pygame_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == self.keys['up']:
				self.jumping = True
		elif event.type == pygame.KEYUP:
			if event.key == self.keys['up']:
				self.jumping = False
