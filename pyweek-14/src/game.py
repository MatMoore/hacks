'''Core game logic goes here'''

from lib import tmx
from resource import load_image, file_path
import pygame
from logging import info,debug,error

class Game(object):
	'''Main game object to track anything that persists between levels'''
	def __init__(self, viewport):
		self.viewport = viewport
		self.current_level = Level(file_path('map.tmx'), viewport)
		object.__init__(self)

	def update(self, dt):
		debug(dt)

	def draw(self, screen):
		self.current_level.draw(screen)

	def handle_pygame_event(self, event):
		pass

class Level(object):
	def __init__(self, filename, viewport):
		self.tilemap = tmx.load(filename, viewport)
		start_cell = self.tilemap.layers['triggers'].find('player')[0]

		# Add sprite layer to map
		self.sprites = tmx.SpriteLayer()
		self.tilemap.layers.append(self.sprites)
		self.player = Player((start_cell.px, start_cell.py), self.sprites)
		self.tilemap.set_focus(self.player.rect.x, self.player.rect.y)

	def update(self, dt):
		self.tilemap.update(dt)

	def draw(self, screen):
		screen.fill((0, 0,0))
		self.tilemap.draw(screen)
		pygame.display.flip()

class Player(pygame.sprite.Sprite):
	def __init__(self, location, *groups):
		super(Player, self).__init__(*groups)
		self.image = load_image('player.png')
		self.rect = pygame.rect.Rect(location, self.image.get_size())
		self.resting = False
		self.dy = 0
