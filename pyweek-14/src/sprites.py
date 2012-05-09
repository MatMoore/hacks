from lib.tmx import Tile, Tileset, SpriteLayer, Cell, Layers, Tilesets, LayerIterator
from pygame.rect import Rect
import pygame
from config import settings
from resource import load_image, file_path
from logging import info, debug, error

class PlatformLayer(object):
	'''Tile based layer with infinite height and width'''

	def __init__(self):
		self.tileset = Tileset('platforms', 32, 32, 0)
		self.tileset.add_image(file_path('platforms.png'))
		self.tile_width, self.tile_height = (self.tileset.tile_width, self.tileset.tile_height)
		self.cells = {}
		self.visible = True

	def __getitem__(self, pos):
		return self.cells.get(pos)

	def __setitem__(self, pos, tile):
		x, y = pos
		px = x * self.tile_width
		py = y * self.tile_width
		self.cells[pos] = Cell(x, y, px, py, tile)

	def __iter__(self):
		return LayerIterator(self)

	def update(self, dt):
		self._remove_assimilated()

	def _remove_assimilated(self):
		'''Remove stuff covered by goo'''
		# view_y is getting more negative over time
		# so we can remove anything more positive
		return
		max_height = self.view_y / self.tile_height
		for (i, j) in self.cells.keys():
			if j > max_height:
				del self.cells[(i, j)]

	def set_view(self, x, y, w, h, viewport_ox=0, viewport_oy=0):
		debug('set_view %d %d' % (x, y))
		self.view_x, self.view_y = x, y
		self.view_w, self.view_h = w, h
		x -= viewport_ox
		y -= viewport_oy
		self.position = (x, y)

	def draw(self, surface):
		'''Draw this layer, limited to the current viewport, to the Surface.
		'''
		ox, oy = self.position
		w, h = self.view_w, self.view_h
		for x in range(ox, ox+w+self.tile_width, self.tile_width):
			i = x // self.tile_width
			for y in range(oy, oy+h+self.tile_height, self.tile_height):
				j = y // self.tile_height
				if (i, j) not in self.cells:
					continue
				cell = self.cells[i, j]
				surface.blit(cell.tile.surface, (cell.px-ox, cell.py-oy))

		# TODO draw walls

	def find(self, *properties):
		'''Find all cells with the given properties set.
		'''
		r = []
		for propname in properties:
			for cell in self.cells.values():
				if cell and propname in cell:
					r.append(cell)
		return r

	def match(self, **properties):
		'''Find all cells with the given properties set to the given values.
		'''
		r = []
		for propname in properties:
			for cell in self.cells.values():
				if propname not in cell:
					continue
				if properties[propname] == cell[propname]:
					r.append(cell)
		return r

	def collide(self, rect, propname):
		'''Find all cells the rect is touching that have the indicated property
		name set.
		'''
		r = []
		for cell in self.get_in_region(rect.left, rect.top, rect.right, rect.bottom):
			if not cell.intersects(rect):
				continue
			if propname in cell:
				r.append(cell)
		return r

	def get_in_region(self, x1, y1, x2, y2):
		'''Return cells (in [column][row]) that are within the map-space
		pixel bounds specified by the bottom-left (x1, y1) and top-right
		(x2, y2) corners.

		Return a list of Cell instances.
		'''
		i1 = max(0, x1 // self.tile_width)
		j1 = max(0, y1 // self.tile_height)
		i2 = x2 // self.tile_width + 1
		j2 = y2 // self.tile_height + 1
		return [self.cells[i, j]
			for i in range(int(i1), int(i2))
				for j in range(int(j1), int(j2))
					if (i, j) in self.cells]

	def get_at(self, x, y):
		'''Return the cell at the nominated (x, y) coordinate.

		Return a Cell instance or None.
		'''
		i = x // self.tile_width
		j = y // self.tile_height
		return self.cells.get((i, j))

	def neighbors(self, index):
		'''Return the indexes of the valid (ie. within the map) cardinal (ie.
		North, South, East, West) neighbors of the nominated cell index.

		Returns a list of 2-tuple indexes.
		'''
		i, j = index
		n = []
		n.append((i+1, j))
		n.append((i-1, j))
		n.append((i, j+1))
		n.append((i, j-1))
		return n

class Player(pygame.sprite.Sprite):
	def __init__(self, location, *groups):
		pygame.sprite.Sprite.__init__(self, *groups)
		self.image = load_image('player.png')
		self.rect = pygame.rect.Rect(location, self.image.get_size())
		self.resting = False
		self.dy = 0
		self.speed = settings.getfloat('Physics', 'run_speed')

	def left(self, dt):
		self.rect.left -= self.speed * dt

	def right(self, dt):
		self.rect.left += self.speed * dt


class Camera(object):
    '''This is totally cannibalised from the tmx library's TileMap.
    Here it just acts as a viewport onto multiple layers.

   tile_width, tile_height - the dimensions of the cells in the map
   layers - all layers of this tilemap as a Layers instance
   fx, fy - viewport focus point
   view_w, view_h - viewport size
   view_x, view_y - viewport offset (origin)
   viewport - a Rect instance giving the current viewport specification
   '''
    def __init__(self, size, origin=(0,0)):
        self.px_width = 0
        self.tile_width = 0
        self.tile_height = 0
        self.layers = Layers()
        self.fx, self.fy = 0, 0             # viewport focus point
        self.view_w, self.view_h = size     # viewport size
        self.view_x, self.view_y = origin   # viewport offset
        self.viewport = Rect(origin, size)
        self._old_focus = None

    def update(self, dt, *args):
        for layer in self.layers:
            layer.update(dt, *args)

    def draw(self, screen):
        for layer in self.layers:
            if layer.visible:
                layer.draw(screen)

    def set_focus(self, fx, fy, force=False):
        '''Determine the viewport based on a desired focus pixel in the
        Layer space (fx, fy) and honoring any bounding restrictions of
        child layers.

        The focus will always be shifted to ensure no child layers display
        out-of-bounds data, as defined by their dimensions px_width and px_height.
        '''
        # The result is that all chilren will have their viewport set, defining
        # which of their pixels should be visible.
        fx, fy = int(fx), int(fy)
        self.fx, self.fy = fx, fy

        a = (fx, fy)

        # check for NOOP (same arg passed in)
        if not force and self._old_focus == a:
            return
        self._old_focus = a

        debug('set focus %d %d' % (fx, fy))

        # get our viewport information, scaled as appropriate
        w = int(self.view_w)
        h = int(self.view_h)
        w2, h2 = w//2, h//2

        if self.px_width <= w:
            # this branch for centered view and no view jump when
            # crossing the center; both when world width <= view width
            restricted_fx = self.px_width / 2
        else:
            if (fx - w2) < 0:
                restricted_fx = w2       # hit minimum X extent
            elif (fx + w2) > self.px_width:
                restricted_fx = self.px_width - w2       # hit maximum X extent
            else:
                restricted_fx = fx

        restricted_fy = fy

        # ... and this is our focus point, center of screen
        self.restricted_fx = restricted_fx
        self.restricted_fy = restricted_fy

        # determine child view bounds to match that focus point
        x, y = restricted_fx - w2, restricted_fy - h2
        self.viewport.x = x
        self.viewport.y = y

        self.childs_ox = x - self.view_x
        self.childs_oy = y - self.view_y

        for layer in self.layers:
            layer.set_view(x, y, w, h, self.view_x, self.view_y)

    def pixel_from_screen(self, x, y):
        '''Look up the Layer-space pixel matching the screen-space pixel.
        '''
        vx, vy = self.childs_ox, self.childs_oy
        return int(vx + x), int(vy + y)

    def pixel_to_screen(self, x, y):
        '''Look up the screen-space pixel matching the Layer-space pixel.
        '''
        screen_x = x-self.childs_ox
        screen_y = y-self.childs_oy
        return int(screen_x), int(screen_y)

    def index_at(self, x, y):
        '''Return the map index at the (screen-space) pixel position.
        '''
        sx, sy = self.pixel_from_screen(x, y)
        return int(sx//self.tile_width), int(sy//self.tile_height)
