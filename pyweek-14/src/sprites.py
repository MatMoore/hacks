from .lib.tmx import Tile, Tileset, SpriteLayer, Cell, Layers, Tilesets, LayerIterator
from pygame.rect import Rect
import pygame
from .config import settings
from .resource import load_image, file_path
from logging import info, debug, error
from .resource import load_font, play_sound
from numpy.random import randint

def draw_fg(surface, player, level, height):
	font = load_font('VeraMono.ttf', 32)
	font2 = load_font('VeraMono.ttf', 48)
	font3 = load_font('VeraMono.ttf', 20)

	jetpack_percent = min(1.0, float(player.jetpack_time)/player.max_jetpack)
	text = font.render('%2.f' % (jetpack_percent * 100), True, (int(255 - jetpack_percent * 255), 0, 0))
	x = surface.get_width()-text.get_width() - 10
	y = 10
	surface.blit(text, (x, y))

	text = font2.render(str(level), True, (0, 0, 150))
	surface.blit(text, (10, 10))
	text = font3.render(str(height), True, (0, 0, 150))
	surface.blit(text, (12, 60))

class Animation(object):
	def __init__(self, surface, width, total_time):
		self.frames = []
		height = surface.get_height()
		for x in range(0, surface.get_width()-1, width):
			rect = Rect(x, 0, width, height)
			self.frames.append(surface.subsurface(rect))
		self.total_time = total_time
		self.frame_time = float(total_time) / len(self.frames)
		self.t = 0

	@property
	def current(self):
		frame = int(self.t / self.frame_time)
		return self.frames[frame]

	def update(self, dt):
		self.t = (self.t + dt) % self.total_time

class Powerup(pygame.sprite.Sprite):
	sprites = {
			'double_speed': 'rainbow.png',
			'half_speed': 'yellow.png',
			'half_gravity': 'purple.png',
			'double_jetpack': 'orange.png',
			'reverse_keys': 'pink.png',
	}
	def __init__(self, location, powerup, *groups):
		pygame.sprite.Sprite.__init__(self, *groups)
		self.image = load_image(self.sprites[powerup])
		self.rect = pygame.rect.Rect(location, self.image.get_size())
		self.name = powerup

class GooLayer(object):
	def __init__(self):
		self.level = 300
		self.goo_speed = 0.1
		self.visible = True

	def update(self, dt):
		self.level -= self.goo_speed * dt

	def set_view(self, x, y, w, h, viewport_ox=0, viewport_oy=0):
		y -= viewport_oy
		self.position = y
		self.level = min(self.level, self.position+700)

	def draw(self, screen, tilesize=100):
		rect = screen.get_rect()
		if self.level > self.position:
			rect.top = self.level - self.position
		goo = pygame.Surface((tilesize, tilesize))
		size = (tilesize, tilesize, 3)
		goopx = randint(100, 175, size=size)
		try:
			pygame.surfarray.blit_array(goo, goopx)
			for x in range(rect.left, rect.width, tilesize):
				for y in range(rect.top, rect.height, tilesize):
					screen.blit(goo, (x, y))
		except NotImplementedError:
			screen.fill((120,120,120), rect)


#		screen.fill((200, 200, 200), rect)

class PlatformLayer(object):
	'''Tile based layer with infinite height and fixed width'''

	def __init__(self, width, tileset):
		self.tileset = tileset
		self.tile_width, self.tile_height = (self.tileset.tile_width, self.tileset.tile_height)
		self.cells = {}
		self.visible = True
		self.width = width

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
		pass

	def remove_assimilated(self, goo_level):
		'''Remove stuff covered by goo'''
		max_height = goo_level / self.tile_height
		for (i, j) in list(self.cells.keys()):
			if j > max_height:
				debug('platform consumed')
				del self.cells[(i, j)]

	def set_view(self, x, y, w, h, viewport_ox=0, viewport_oy=0):
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
					if i == 0 or i >= self.width-1:
						self.draw_wall(surface, i, j)
					continue
				cell = self.cells[i, j]
				surface.blit(cell.tile.surface, (cell.px-ox, cell.py-oy))

	def draw_wall(self, surface, i, j):
		ox, oy = self.position
		px = i * self.tile_width
		py = j * self.tile_width
		tile = self.tileset.get_tile(0)
		surface.blit(tile.surface, (px-ox, py-oy))

	def collide_wall(self, rect):
		rightedge = (self.width -1) * self.tile_width
		if rect.left < self.tile_width:
			rect.left = self.tile_width
		elif rect.right >= rightedge:
			rect.right = rightedge

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
		i1 = x1 // self.tile_width
		j1 = y1 // self.tile_height
		i2 = x2 // self.tile_width + 1
		j2 = y2 // self.tile_height + 1
		return [self.cells[i, j] \
			for i in range(int(i1), int(i2)) \
				for j in range(int(j1), int(j2)) \
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
		self.running = Animation(load_image('player-normal.png'), 20, 100)
		self.flying = Animation(load_image('player-jetpack.png'), 20, 100)
		self.running_l = Animation(load_image('player-normal-l.png'), 20, 100)
		self.flying_l = Animation(load_image('player-jetpack-l.png'), 20, 100)
		self.resting = False
		self.face_right = True
		self.rect = pygame.rect.Rect(location, self.image.get_size())
		self.dy = 0
		self.speed = settings.getfloat('Physics', 'run_speed')
		self.max_jetpack = settings.getint('Physics', 'jetpack_time')
		self.jump_speed = settings.getfloat('Physics', 'jump_speed')
		self.jetpack_accn = settings.getfloat('Physics', 'jetpack_accn')
		self.jetpack_time = self.max_jetpack
		self.recharge_rate = self.max_jetpack / settings.getfloat('Physics', 'jetpack_recharge_time')
		self.gravity = settings.getfloat('Physics', 'gravity')
		self.terminal_velocity = settings.getfloat('Physics', 'terminal_velocity')

	def left(self, dt):
		self.rect.left -= self.speed * dt
		self.face_right = False

	def right(self, dt):
		self.rect.left += self.speed * dt
		self.face_right = True

	@property
	def image(self):
		if self.resting:
			if self.face_right:
				return self.running.current
			else:
				return self.running_l.current
		else:
			if self.face_right:
				return self.flying.current
			else:
				return self.flying_l.current

	def jump(self):
		# Initial jump
		if self.resting:
			debug('boing')
			play_sound('jetpack.wav')
			self.resting = False
			self.dy = -self.jump_speed

	def up(self, dt):
		if self.resting:
			# Jump must occur first
			return

		# Jetpack acceleration
		if self.jetpack_time > 0:
			debug('woosh')
			jetpack_time = min(dt, self.jetpack_time)
			self.dy -= self.jetpack_accn * jetpack_time
			self.jetpack_time -= jetpack_time

	def endjump(self):
		self.resting = True
		self.dy = 0

	def update(self, dt):
		self.running.update(dt)
		self.running_l.update(dt)
		self.flying.update(dt)
		self.flying_l.update(dt)

		if self.resting:
			# Recharge jetpack
			self.jetpack_time = min(self.max_jetpack,
					self.jetpack_time + self.recharge_rate * dt)
		else:
			# Gravity
			self.dy += self.gravity * dt
			self.dy = min(self.dy, self.terminal_velocity)
			self.dy = max(self.dy, -self.terminal_velocity)

			# Oh hi inertia
			self.rect.top += self.dy * dt


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

        # get our viewport information, scaled as appropriate
        w = int(self.view_w)
        h = int(self.view_h)
        w2, h2 = w//2, h//2

        restricted_fx = w2
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
