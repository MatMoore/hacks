'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import data
import json
import curses
import random
from curses import textpad

MAP_HEIGHT = 20
MAP_WIDTH = 80
PAD_HEIGHT = 18
PAD_WIDTH = 78

class Map:
	def __init__(self,size):
		self.map = {}
		self.items = {}
		self.width,self.height = size
		for i in range(self.height):
			for j in range(self.width):
				self.map[(i,j)] = '##'
		self.generate()
		self.generateRoom((self.height/2,0)) # generate a room where the player starts
		for i in range(15):
			self.generateRoom((random.randint(0,self.height),random.randint(0,self.width)))
		self.map[(self.height/2-1,0)] = '| ' # the door
		self.map[(self.height/2,0)] = '| ' # the door

		self.emptySpaces = []
		startPoint = (self.height/2,0)
		for point,value in self.map.iteritems():
			if point != startPoint and value == '  ':
				self.emptySpaces.append(point)
		random.shuffle(self.emptySpaces)

	def __iter__(self):
		return self.map.iteritems()

	def __str__(self):
		s = ''
		for i in range(self.height):
			for j in range(self.width):
				s += self.map[(i,j)]
			s += '\n'
		return s

	def neighbours(self,point):
		y,x = point
		n = []
		if x > 0:
			n.append((y,x-1))
		if x < self.width - 1:
			n.append((y,x+1))
		if y > 0:
			n.append((y-1,x))
		if y < self.height - 1:
			n.append((y+1,x))
		return n

	def generateRoom(self,point):
		centrey,centrex = point
		width = random.randint(6,10)
		height = random.randint(3,5)
		top = centrey-height/2
		bottom = centrey+(height+1)/2
		left = centrex-width/2
		right = centrex+(width+1)/2
		for y in range(top,bottom):
			for x in range(left,right):
				self.map[(y,x)] = '  '
		return ((top,left),(bottom,right))

	def generate(self):
		'''Generate a maze'''
		start = (self.height/2,0) # this is where the door will be
		passages = [start]

		while passages:
			passage = passages.pop()
			walls = self.neighbours(passage)

			surroundingSpace = 0
			for wall in walls:
				if self.map[wall] == '  ':
					surroundingSpace += 1
			if surroundingSpace > 1:
				continue

			self.map[passage] = '  '

			random.shuffle(walls)
			for wall in walls:
				if self.map[wall] != '  ' and wall not in passages:
					passages.append(wall) # branch out from this passage

	def placeItem(self,item):
		if self.emptySpaces:
			point = self.emptySpaces.pop()
			self.items[point] = item

class Game:
	def __init__(self,name='Player 2'):
		self.name = name
		self.map = Map((40,20))
		self.playerLocation = (self.map.height/2,1)
		self.inventory = []
		self.lastMove = 'n'
		self.loadItems()

	def loadItems(self):
		f = data.load('items2.json')
		items = json.load(f)
		self.items = {}
		self.combinations = {}
		self.interactions = {}
		for i in items['items']:
			if i['available']:
				self.items[i['name'].lower()] = i
				self.map.placeItem(i)
	
		for i in items['combinations']:
			self.combinations[frozenset(i['items'])] = i['product']

		for i in items['interactions']:
			self.interactions[frozenset(i['items'])] = i['message']

	def look(self,item=None):
		items = []
		if self.playerLocation in self.map.items:
			items.append(self.map.items[self.playerLocation]['name'])
		for point in self.map.neighbours(self.playerLocation):
			if point in self.map.items:
				items.append(self.map.items[point]['name'])
		if item is not None:
			if item in items:
				return self.items[item]['description']
			else:
				return None
		s = 'You are trapped inside a half finished pyweek entry.'
		if items:
			s += ' Nearby you can see: '+', '.join(items)
		return s

	def pickup(self,item):
		pass

	def drop(self,item):
		pass

class Console:
	def __init__(self,screen):
		self.mode = 'move'
		self.screen = screen
		self.textwin = curses.newwin(1,78,21,1)
#		self.outputwin = curses.newwin(3,80,23,0)
		textpad.rectangle(self.screen,0,0,20,80)
		textpad.rectangle(self.screen,20,0,22,80)
		self.pad = curses.newpad(20,80)
		self.textpad = textpad.Textbox(self.textwin)
		self.game = Game()
		self.output = ''
		self.redraw()
	
	def redraw(self):
		self.screen.redrawln(23,10)
		if self.mode == 'insert':
			curses.curs_set(1)
		else:
			curses.curs_set(0)
		for k,v in self.game.map:
			y,x = k

			if k in self.game.map.items:
				v = self.game.map.items[k]['gfx']

			v1 = v[0]
			v2 = ' '
			if len(v)>1:
				v2 = v[1]
			try:
				self.pad.addch(y,x*2, ord(v1))
			except: pass
			try:
				self.pad.addch(y,x*2+1, ord(v2))
			except: pass

		# draw player over the top of everything else
		y,x = self.game.playerLocation
		try:
			self.pad.addch(y,x*2,   ord('/'))
		except:
			pass
		try:
			self.pad.addch(y,x*2+1,   ord('\\'))
		except:
			pass
		try:
			self.pad.addch(y-1,x*2,   ord('o'))
		except:
			pass
		try:
			self.pad.addch(y-1,x*2+1,   ord('_'))
		except:
			pass
		try:
			self.pad.addch(y-1,x*2-1,   ord('_'))
		except:
			pass

		# Show the area around the player
		self.screen.addstr(23,0,' '*300)
		self.screen.addstr(23,0,self.output)
		#if len(self.output) <80:
			#			self.screen.addstr(23,len(self.output),' '*(80-len(self.output))) #hack because I don't know what im doing
		cameray,camerax = self.game.playerLocation
		cameray = min(max(0,cameray - PAD_HEIGHT/2),MAP_HEIGHT-PAD_HEIGHT)
		camerax = min(max(0,camerax - PAD_WIDTH/2),MAP_WIDTH-PAD_WIDTH)
		self.pad.refresh(cameray,camerax, 1,1,PAD_HEIGHT,PAD_WIDTH)
		self.screen.refresh()

	def run(self):
		self.redraw()
		while True:
			if self.mode == 'insert':
				command = self.textpad.edit()
				self.doCommand(command)
				self.mode = 'move'
			else:
				c = self.screen.getch()
				if c == ord('q'): break
				elif c == curses.KEY_LEFT:
					left = (self.game.playerLocation[0],self.game.playerLocation[1]-1)
					if left[1] >= 0 and self.game.map.map[left] == '  ':
						self.game.playerLocation = left
				elif c == curses.KEY_RIGHT:
					right = (self.game.playerLocation[0],self.game.playerLocation[1]+1)
					if right[1] < self.game.map.width and self.game.map.map[right] == '  ':
						self.game.playerLocation = right
				elif c == curses.KEY_UP:
					up = (self.game.playerLocation[0]-1,self.game.playerLocation[1])
					if up[0] >= 0 and self.game.map.map[up] == '  ':
						self.game.playerLocation = up
				elif c == curses.KEY_DOWN:
					down = (self.game.playerLocation[0]+1,self.game.playerLocation[1])
					if down[0] < self.game.map.height and self.game.map.map[down] == '  ':
						self.game.playerLocation = down
				elif c == ord('i') or c == ord('I'):
					self.mode = 'insert'
			self.redraw()

	def doCommand(self,command):
		self.output = ''
		words = command.split()
		if not words:
			return

		if words[0].lower() == 'help':
			self.output = 'No help is available'
		if words[0].lower() == 'look':
			if len(words[1:]):
				desc = self.game.look(" ".join(words[1:]).lower())
				if desc is not None:
					self.output = desc
				else:
					self.output = 'I don\'t see any '+" ".join(words[1:])
			else:
				self.output = self.game.look()

def show(screen):
	c = Console(screen)
	c.run()

def main():

	game = Game()
	#	print str(game.map)
	#	print '\nItems:'
	#	for i in game.items:
	#		print str(i)
	#
	#	print '\nCombinations'
	#	for i,j in game.combinations.iteritems():
	#		print str(i) + ' -> ' + str(j)
	#
	#	print '\nInteractions'
	#	for i,j in game.interactions.iteritems():
	#		print str(i) + ' -> ' + str(j)

	curses.wrapper(show)
