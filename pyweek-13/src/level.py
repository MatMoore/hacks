from lib.tiledtmxloader import tiledtmxloader
from lib.tiledtmxloader.helperspygame import ResourceLoaderPygame, RendererPygame
import resource
import os
import pygame
from logging import info,debug,error
from util import debug1,throttle

def level_path(filename):
	return os.path.join(resource.data_path(), 'levels', filename)

class Player(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = resource.load_image('player000.png')
		self.speed = 100.0
		self.velocity = (0,0)

		# Position within the level
		self.rect = pygame.Rect(pos, self.image.get_size())

	def set_direction(self, x, y):
		x*= self.speed
		y*= self.speed
		self.velocity = (x,y)

	def move(self, ms):
		s = ms/1000.0
		dx, dy = self.velocity
		dx *= s
		dy *= s
		self.rect.left += dx
		self.rect.top += dy
		self.debug()

	@throttle(50)
	def debug(self):
		debug('position = %s', self.rect)
		debug('velocity = %s', self.velocity)


class Level(object):
	'''This object is responsible for drawing the level and everything in it'''
	def __init__(self, filename, screen_width, screen_height):
		object.__init__(self)
		filename = level_path(filename)
		self.player = Player((0, 0))
		self.camera = pygame.Rect((0,0), (screen_width, screen_height))
		world_map = tiledtmxloader.TileMapParser().parse_decode(filename)
		resources = ResourceLoaderPygame()
		resources.load(world_map)
		self.renderer = RendererPygame(resources)
		self.renderer.set_camera_position_and_size(0, 0, screen_width, screen_height)
		self.renderer.set_camera_margin(0, 0, 0, 0)
		self.screen_width = screen_width
		self.screen_height = screen_height

	def collide_wall(self):
		# get player collision rect
		# divide up into tiles
		# check each for stuff
		for tile in tiles:
			sprites=pick_layers_sprites()

	def input_changed(self, action, state):
		x = 0
		y = 0
		if state['up']:
			y = -1
		elif state['down']:
			y = 1
		if state['left']:
			x = -1
		elif state['right']:
			x = 1
		self.player.set_direction(x,y)

	def tick(self, ms):
		self.player.move(ms)
		self.camera.center = self.player.rect.center

		# Constrain camera to the level
		self.camera.right = min(self.camera.right, self.screen_width)
		self.camera.bottom = min(self.camera.right, self.screen_height)
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
			if 0 and sprite_layer.is_object_group:
				self._draw_obj_group(screen, sprite_layer, cam_world_pos_x, cam_world_pos_y)
			else:
				self.renderer.render_layer(screen, sprite_layer)

		player_pos = self.screen_coordinates(self.player.rect.topleft)
		debug1('playerpos=%s', player_pos)

		screen.blit(self.player.image, player_pos)

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
