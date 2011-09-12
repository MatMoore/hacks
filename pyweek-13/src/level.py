from lib.tiledtmxloader import tiledtmxloader
from lib.tiledtmxloader.helperspygame import ResourceLoaderPygame, RendererPygame
import resource
import os
import pygame

def level_path(filename):
	return os.path.join(resource.data_path(), 'levels', filename)

class Level(object):
	'''This object is responsible for drawing the level and everything in it'''
	def __init__(self, filename, screen_width, screen_height):
		object.__init__(self)
		filename = level_path(filename)
		self._camera = (0, 0)
		cx, cy = self._camera
		world_map = tiledtmxloader.TileMapParser().parse_decode(filename)
		resources = ResourceLoaderPygame()
		resources.load(world_map)
		self.renderer = RendererPygame(resources)
		self.renderer.set_camera_position_and_size(cx, cy, screen_width, screen_height)

	def tick(self, ms):
		#self.renderer.set_camera_position(cam_world_pos_x, cam_world_pos_y)
		pass

	def draw(self, screen):
		screen.fill((255,255,255))
		sprite_layers = self.renderer.get_layers_from_map()
		for sprite_layer in sprite_layers:
			if 0 and sprite_layer.is_object_group:
				self._draw_obj_group(screen, sprite_layer, cam_world_pos_x, cam_world_pos_y)
			else:
				self.renderer.render_layer(screen, sprite_layer)
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
