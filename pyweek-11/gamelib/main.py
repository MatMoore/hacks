'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import data
import json
import curses
import random

class Map:
	def __init__(self,size):
		self.map = {}
		self.width,self.height = size
		for i in range(self.height):
			for j in range(self.width):
				self.map[(i,j)] = '##'
		self.generate()
		self.generateRoom((self.height/2,0)) # generate a room where the player starts
		for i in range(15):
			self.generateRoom((random.randint(0,self.height),random.randint(0,self.width)))
		self.map[(self.height/2,0)] = ']-' # the door

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
		'''Generate a dungeon'''
		start = (self.height/2,0) # this is where the door will be
#		tl,br = self.generateRoom(start)
#		edge = self.randomEdge(tl,br)
#		if not edge:
#			return

		# make a maze
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

	def spawnItems(items):
		pass

class Game:
	def __init__(self,name='Player 2'):
		self.name = name
		self.map = Map((40,20))
		self.playerLocation = (self.map.width/2, self.map.height/2)
		self.inventory = []
		self.lastMove = 'n'
		self.loadItems()

	def loadItems(self):
		f = data.load('items2.json')
		items = json.load(f)
		self.items = items['items']
		self.combinations = {}
		self.interactions = {}
		for i in items['combinations']:
			self.combinations[frozenset(i['items'])] = i['product']

		for i in items['interactions']:
			self.interactions[frozenset(i['items'])] = i['message']

	def look():
		pass

	def pickup(item=None):
		pass

	def drop(item):
		pass

	def theOtherWay(self,direction):
		if direction.lower() in ('n','north','up','that way'):
			return 's'
		elif direction.lower() in ('s','south','down','this way'):
			return 'n'
		elif direction.lower() in ('e','right','east'):
			return 'w'
		elif direction.lower() in ('w','left','west'):
			return 'e'

	def move(direction):
		if direction == 'forward':
			direction = self.lastMove
		elif direction == 'backward':
			direction = self.theOtherWay(self.lastMove)
		if direction.lower() in ('n','north','up','that way'):
			pass
		elif direction.lower() in ('s','south','down','this way'):
			pass
		elif direction.lower() in ('e','right','east'):
			pass
		elif direction.lower() in ('w','left','west'):
			pass

class Item():
	def __init__(self,definition):
		self.name = definition['name']
		self.description = definition['description']
		self.gfx = definition['gfx']

class Console:
	def __init__(self,screen):
		self.screen = screen
		self.pad = curses.newpad(100,100)
		self.redraw()
	
	def redraw(self):
		# Draw the map
		for y in range(0,100):
			for x in range(0,100):
				try:
					self.pad.addch(y,x, ord('a')+(x*x+y*y)%26)
				except:
					pass

		# Show the area around the player
		self.pad.refresh(0,0, 5,5,20,75)
		self.screen.refresh()

	def run(self):
		self.redraw()
		while True:
			c = self.screen.getch()
			if c == ord('q'): break
			self.redraw()

def show(screen):
	c = Console(screen)
	c.run()

def main():
	print "Hello from your game's main()"

	game = Game()
	print str(game.map)
	print '\nItems:'
	for i in game.items:
		print str(i)

	print '\nCombinations'
	for i,j in game.combinations.iteritems():
		print str(i) + ' -> ' + str(j)

	print '\nInteractions'
	for i,j in game.interactions.iteritems():
		print str(i) + ' -> ' + str(j)

	#curses.wrapper(show)
