from lib.tiledtmxloader import tiledtmxloader
from lib.tiledtmxloader.helperspygame import ResourceLoaderPygame, RendererPygame
import resource
import os
import pygame
from logging import info,debug,error
from util import debug1,throttle,Timer
import config
from math import floor

class OutOfBounds(Exception):
	pass

class Death(Exception):
	pass

class FellOffMap(Death):
	pass

def level_path(filename):
	return os.path.join(resource.data_path(), 'levels', filename)

class Player(pygame.sprite.Sprite):
	'''
	Player is max 32x32 px whereas tiles are 16px
	Need to ensure that the player cannot move more than 16px per frame
	to avoid tunnelling
	'''
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = resource.load_image('player000.png')
		self.speed = 100.0
		self.velocity = (0,0)

		# Position within the level
		self.rect = pygame.Rect(pos, self.image.get_size())

	@property
	def collide_rect(self):
		rect = self.rect.move((8,16))
		rect.width=16
		rect.height=16
		return rect

	@property
	def bottom_collide_pts(self):
		y = self.collide_rect.bottom
		for x in range(self.collide_rect.left+8, self.collide_rect.right, 16):
			yield (x,y)

	@property
	def top_collide_pts(self):
		y = self.collide_rect.top
		for x in range(self.collide_rect.left+8, self.collide_rect.right, 16):
			yield (x,y)

	@property
	def left_collide_pts(self):
		x = self.collide_rect.left
		for y in range(self.collide_rect.top+8, self.collide_rect.bottom, 16):
			yield (x,y)

	@property
	def right_collide_pts(self):
		x = self.collide_rect.right
		for y in range(self.collide_rect.top+8, self.collide_rect.bottom, 16):
			yield (x,y)

	def set_direction(self, x):
		x*= self.speed
		self.velocity = (x, self.velocity[1])

	def move(self, ms):
		s = ms/1000.0
		dx, dy = self.velocity

		# obey gravity
		dy += config.getfloat('Physics','gravity') * s
		dy = min(config.getfloat('Physics','terminal_velocity'), dy)
		self.velocity = dx,dy

		dx *= s
		dy *= s

		# Hard limit on speed
		v = (dx **2 + dy**2) ** 0.5
		if v > 15:
			dx = floor(dx * 15.0 / v)
			dy = floor(dy * 15.0 / v)

		self.rect.left += dx
		self.rect.top += dy
		self.debug()

	@throttle(50)
	def debug(self):
		debug('position = %s', self.rect)
		debug('velocity = %s', self.velocity)


class JumpTimer(object):
	def __init__(self):
		object.__init__(self)
		self.timer = None
	
	def set(self):
		# Add a 100ms timer
		self.timer = Timer(config.getint('Physics','jump_time'))
	
	def update(self, ms):
		# Remove timer when time runs out
		if self.timer and self.timer.check(ms):
			self.unset()

	def jump_allowed(self):
		return self.timer is not None

	def unset(self):
		self.timer = None

class Level(object):
	'''This object is responsible for drawing the level and everything in it'''
	def __init__(self, filename, screen_width, screen_height):
		object.__init__(self)
		filename = level_path(filename)
		self.player = Player((50, 50))
		self.camera = pygame.Rect((50,50), (screen_width, screen_height))
		self.world_map = tiledtmxloader.TileMapParser().parse_decode(filename)
		resources = ResourceLoaderPygame()
		resources.load(self.world_map)
		self.renderer = RendererPygame(resources)
		self.renderer.set_camera_position_and_size(0, 0, screen_width, screen_height)
		self.renderer.set_camera_margin(0, 0, 0, 0)
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.jump_timer = JumpTimer()
		self.input_state = None

	def restart(self):
		self.player.rect.topleft=(50,50)
		self.player.velocity = (0,0)

	def collide_walls(self, ms):
		grounded = False
		for layer in self.world_map.layers:
			if layer.is_object_group:
				continue
			for pos in self.player.bottom_collide_pts:
				if self.get_tile(pos, layer):
					# Move above this tile.
					# This assumes we are not completely overlapping a tile.
					# This should never happen if we limit movement to < 16px per frame
					self.player.rect.bottom -= (self.player.collide_rect.bottom) % 16
					grounded = True
					break

			top_points = self.player.top_collide_pts
			for pos in top_points:
				if grounded: break
				if self.get_tile(pos, layer):
					debug('collide top %s', pos)
					self.player.rect.top += 16 # move one tile down
					self.player.rect.top -= self.player.collide_rect.top % 16 # move to the top of the tile
					break

			left_points = self.player.left_collide_pts
			for pos in left_points:
				if self.get_tile(pos, layer):
					debug('collide left %s', pos)
					self.player.rect.left += 16
					self.player.rect.left -= self.player.collide_rect.left % 16
					break

			right_points = self.player.right_collide_pts
			for pos in right_points:
				if self.get_tile(pos, layer):
					debug('collide right %s', pos)
					debug(self.get_tile(pos,layer))
					self.player.rect.right -= (self.player.collide_rect.right ) % 16
					break

		# Update the jump timer which determines if it's possible to jump
		if grounded:
			self.jump_timer.set()
		else:
			self.jump_timer.update(ms)
	
	def get_tile(self, pos, layer):
		x,y = pos
		if x < 0 or y < 0  or x >= layer.pixel_width or y >= layer.pixel_height:
			raise OutOfBounds()
		x /= 16
		y /= 16
		tile = layer.decoded_content[x + y*layer.width]
		return tile

	def input_changed(self, action, state):
		x = 0
		if state['left']:
			x = -1
		elif state['right']:
			x = 1
		self.player.set_direction(x)

		self.input_state = state

	def tick(self, ms):
		self.player.move(ms)

		debug1('end of world=%s', self.world_map.pixel_width-16-1)
		if self.player.collide_rect.left >= self.world_map.pixel_width - 16:
			debug('Level complete')
			return True

		# Check for jump every frame, in case user is holding down the button
		if self.input_state and self.input_state['up'] and self.jump_timer.jump_allowed():
			debug('jump')
			self.jump_timer.unset()
			self.player.velocity = (self.player.velocity[0], -config.getfloat('Physics', 'jump_speed'))

		# Handle collisions with walls/platforms
		try:
			self.collide_walls(ms)
		except OutOfBounds:
			debug('%s out of bounds', self.player.collide_rect)
			raise FellOffMap()

		# Center camera on player
		self.camera.center = self.player.rect.center

		# Constrain camera to the level
		self.camera.right = min(self.camera.right, self.world_map.pixel_width)
		self.camera.bottom = min(self.camera.bottom, self.world_map.pixel_height)
		self.camera.left = max(self.camera.left, 0)
		self.camera.top = max(self.camera.top, 0)
		self.renderer.set_camera_position(self.camera.centerx, self.camera.centery)
		self.renderer.set_camera_margin(0, 0, 0, 0) # something is resetting the margin to 16px each frame... grrr

	def debug(self):
		debug('camera %s %s', self.camera.topleft,self.camera.bottomright)
		sprite_layers = self.renderer.get_layers_from_map()
		for sprite_layer in sprite_layers:
			debug('layer %s: margin %s, cam rect %s, render cam rect %s, paralax factor %s,%s',
					id(sprite_layer),
					self.renderer._margin,
					self.renderer._cam_rect,
					self.renderer._render_cam_rect,
					sprite_layer.paralax_factor_x,
					sprite_layer.paralax_factor_y)

	def screen_coordinates(self, pos):
		'''Convert world coordinates into screen coordinates'''
		x,y = pos
		return (x-self.camera.left, y-self.camera.top)

	def draw(self, screen):
		screen.fill((255,255,255))
		sprite_layers = self.renderer.get_layers_from_map()
		for sprite_layer in sprite_layers:
			if sprite_layer.is_object_group:
				self._draw_obj_group(screen, sprite_layer, self.camera.left, self.camera.top)
			else:
				self.renderer.render_layer(screen, sprite_layer)

		screen.blit(self.player.image, self.player.rect.move((-self.camera.left, -self.camera.y)).topleft)

		if config.options.debug:
			pygame.draw.rect(screen, (255,0,0), self.player.collide_rect.move((-self.camera.left, -self.camera.y)), 1)

		pygame.display.flip()

	def _draw_obj_group(self, screen, obj_group, cam_world_pos_x, cam_world_pos_y, font=None):
		goffx = obj_group.x
		goffy = obj_group.y
		for map_obj in obj_group.objects:
			size = (map_obj.width, map_obj.height)
			if map_obj.image_source:
				surf = pygame.image.load(map_obj.image_source)
				surf = pygame.transform.scale(surf, size)
				screen.blit(surf, (goffx + map_obj.x - cam_world_pos_x, \
                          goffy + map_obj.y - cam_world_pos_y))
			#else:
			#	r = pygame.Rect(\
			#		(goffx + map_obj.x - cam_world_pos_x, \
			#		goffy + map_obj.y - cam_world_pos_y),\
      #             size)
			#	pygame.draw.rect(screen, (255, 255, 0), r, 1)
			#	text_img = font.render(map_obj.name, 1, (255, 255, 0))
			#	screen.blit(text_img, r.move(1, 2))

class GameScene(object):
	def __init__(self, levels, director, next_scene=None):
		object.__init__(self)
		self.levels = levels
		self.current = 0
		self.next_scene = next_scene
		self.director = director

		screen_width, screen_height = config.getint('Graphics','width'), config.getint('Graphics', 'height')
		self.level = Level(self.levels[self.current], screen_width, screen_height)

	def new_level(self, level_no=None):
		if level_no is None:
			self.current += 1
		else:
			self.current = level_no
		screen_width, screen_height = config.getint('Graphics','width'), config.getint('Graphics', 'height')
		self.level = Level(self.levels[self.current], screen_width, screen_height)

	def tick(self, ms):
		try:
			completed = self.level.tick(ms)
		except Death:
			self.level.restart()
			return

		if completed:
			if self.current+1 >= len(self.levels):
				debug('Finished game')
				self.director.current = self.next_scene
				return
			else:
				self.new_level()

	def draw(self, *args):
		self.level.draw(*args)

	def input_changed(self, *args):
		self.level.input_changed(*args)
