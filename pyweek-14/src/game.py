'''Core game logic goes here'''

from resource import load_image, file_path, levels, play_sound
import pygame
from logging import info,debug,error
from config import settings
from lib.tmx import Layer, SpriteLayer, Tileset
from sprites import Camera, PlatformLayer, Player, draw_fg, GooLayer, Powerup
from random import randint, random, choice

class Death(Exception):
	pass

class AWinnerIsYou(Exception):
	pass

class Game(object):
	'''Main game object to track anything that persists between levels'''
	def __init__(self, viewport):
		self.viewport = viewport
		object.__init__(self)

		self.tilesize = settings.getint('Graphics', 'tilesize')

		self.goo = GooLayer()
		self.sprites = SpriteLayer()
		self.psprites = SpriteLayer() # powerups

		self.levels = levels()

		self.all_powerups = ['double_speed', 'half_speed', 'half_gravity', 'double_jetpack', 'reverse_keys']

		# Round width/height to nearest tile
		viewport = (viewport[0] / self.tilesize * self.tilesize, viewport[1] / self.tilesize * self.tilesize)
		self.width = viewport[0] / self.tilesize

		tileset = Tileset('platforms', self.tilesize, self.tilesize, 0)
		tileset.add_image(file_path('platforms.png'))
		self.platforms = PlatformLayer(self.width, tileset)

		self.camera = Camera(viewport)
		self.camera.layers.append(self.platforms)
		self.camera.layers.append(self.sprites)
		self.camera.layers.append(self.psprites)
		self.camera.layers.append(self.goo)

		self.reset()

	def reset(self, level=1):
		self.level_no = 0
		for sprite in self.sprites:
			sprite.kill()
		for sprite in self.psprites:
			sprite.kill()
		self.goo.level = 400
		self.player = Player((1, - self.tilesize), self.sprites)
		self.control = PlayerInput(self.player)
		self.powerups = {}
		self.player.rect.bottom = -20
		self.player.rect.left = -10

		self.generate_platform((0, 0), self.width)

		for i in range(level):
			self.next_level()

		self.generate_platform((0, -20), 15)
		self.generate_platform((15, -35), 15)
		self.generate_platform((15, -50), 15)

		self.next_platform = -50 * self.tilesize
		self.last = (15, -50, 15)

	def next_level(self):
		try:
			self.level = self.levels[self.level_no]
			self.level_no += 1
			self.goo.goo_speed = self.level['goo_speed']
			self.target = self.height - 5000
		except IndexError:
			play_sound('win.wav')
			raise AWinnerIsYou()

	@property
	def height(self):
		return self.player.rect.bottom

	def powerup_double_speed(self):
		self.player.speed *= 2

	def powerdown_double_speed(self):
		self.player.speed *= 0.5

	def powerup_half_speed(self):
		self.player.speed *= 0.5

	def powerdown_half_speed(self):
		self.player.speed *= 2

	def powerup_double_gravity(self):
		self.player.gravity *= 1.25

	def powerdown_double_gravity(self):
		self.player.gravity *= 0.8

	def powerup_half_gravity(self):
		self.player.gravity *= 0.5

	def powerdown_half_gravity(self):
		self.player.gravity *= 2

	def powerup_double_jetpack(self):
		self.player.max_jetpack *= 2

	def powerdown_double_jetpack(self):
		self.player.max_jetpack *= 0.5

	def powerup_reverse_keys(self):
		self.control.reverse_keys()

	def powerdown_reverse_keys(self):
		self.control.reverse_keys()

	def add_powerup(self, name):
		info('Go go gadget ' + name + '!')
		self.powerups[name] = 10000
		getattr(self, 'powerup_' + name)()

	def update_powerups(self, dt):
		for k in self.powerups.keys():
			self.powerups[k] -= dt
			if self.powerups[k] < 0:
				del self.powerups[k]
				info('Used up ' + k)
				play_sound('powerdown.wav')
				getattr(self, 'powerdown_' + k)()

	def generate_path(self):
		powerup_rate = self.level['powerup_rate']
		minwidth, maxwidth = (self.level['min_platform_width'],
				self.level['max_platform_width'])
		minjump, maxjump = (self.level['min_jump'],
				self.level['max_jump'])

		lastx, lasty, lastwidth = self.last
		targety = lasty - randint(minjump, maxjump)

		targetwidth = randint(minwidth, maxwidth)
		targetx = randint(0, self.width-targetwidth)

		self.generate_platform((targetx, targety), targetwidth)

		if random() < powerup_rate:
			debug('oh hi powerup')
			offset = randint(0, targetwidth)
			pos = (self.tilesize * (targetx + offset), self.tilesize * (targety-1))
			powerup = Powerup(pos, choice(self.all_powerups), self.psprites)

		# Check that the horizontal distance between platforms is small enough
		dx = min(abs(lastx - targetx), abs((lastx + lastwidth) - (targetx + targetwidth)))
		while dx > 20:
			# Create path to target
			lasty = lasty - maxjump
			if targetx > lastx:
				lastx = lastx + lastwidth/2
				lastwidth = randint(lastwidth, maxwidth)
			else:
				lastx = lastx - lastwidth/2
				lastwidth = randint(lastwidth, maxwidth)
			self.generate_platform((lastx, lasty), lastwidth)
			dx = min(abs(lastx - targetx), abs((lastx + lastwidth) - (targetx + targetwidth)))

		# Generate the next platform once this one becomes visible
		self.next_platform = targety * self.tilesize
		self.last = (targetx, targety, targetwidth)

	def update(self, dt):
		if self.height < self.target:
			self.next_level()

		height_before = self.player.rect.bottom

		# Handle input
		self.control.update(dt)
		self.platforms.collide_wall(self.player.rect)

		# Update platform layer, goo layer, and sprite positions
		self.camera.update(dt)

		# Player can only collide with stuff from above.
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
			play_sound('WilhelmScream.ogg')
			raise Death

		# Pick up powerups
		for powerup in pygame.sprite.spritecollide(self.player, self.psprites, True):
			play_sound('powerup.wav')
			self.add_powerup(powerup.name)

		# Remove used up powerups
		self.update_powerups(dt)

		# Remove old platforms
		self.platforms.remove_assimilated(self.goo.level)

		# Generate out of view platforms
		if self.camera.viewport.top <= self.next_platform:
			self.generate_path()

	def draw(self, screen):
		screen.fill((255, 255, 255))
		self.camera.draw(screen)
		draw_fg(screen, self.player, self.level_no, 0-self.height)
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

	def reverse_keys(self):
		self.keys['left'], self.keys['right'] = (self.keys['right'], self.keys['left'])

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
