from lib.tiledtmxloader import tiledtmxloader
from lib.tiledtmxloader.helperspygame import ResourceLoaderPygame, RendererPygame
import resource
import os
import pygame
from logging import info,debug,error

def level_path(filename):
	return os.path.join(resource.data_path(), 'levels', filename)

class Player(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = resource.load_image('player000.png')

		# Position within the level
		self.rect = pygame.Rect(pos, self.image.get_size())

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
		self.screen_width = screen_width
		self.screen_height = screen_height

	def tick(self, ms):
		self.camera.left = self.player.rect.left
		self.camera.top = self.player.rect.top

		# Constrain camera to the level
		self.camera.right = min(self.camera.right, self.screen_width)
		self.camera.bottom = min(self.camera.right, self.screen_height)
		self.camera.left = max(self.camera.left, 0)
		self.camera.top = max(self.camera.top, 0)

		self.renderer.set_camera_position(self.camera.centerx, self.camera.centery)

	def draw(self, screen):
		screen.fill((255,255,255))
		sprite_layers = self.renderer.get_layers_from_map()
		for sprite_layer in sprite_layers:
			if 0 and sprite_layer.is_object_group:
				self._draw_obj_group(screen, sprite_layer, cam_world_pos_x, cam_world_pos_y)
			else:
				self.renderer.render_layer(screen, sprite_layer)

		screen.blit(self.player.image, (self.player.rect.left - self.camera.left, self.player.rect.top - self.camera.top))

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
