import constants
import pickle
import math
from numpy import *

class Track:
	def __init__(self, loadTrack = None):
		if loadTrack:
			fileHandle = open(loadTrack, 'r')
			self.track = pickle.load(fileHandle)
			self.makeQuads()

	def makeQuads(self):
		pass

	def generateTrack(self, complexity = 10, size = 50):		#complexity defines the number of points for the track, size = the average distance from the center of the map.
		points = []
		for i in range(complexity):
			angle = 2*math.pi * i/complexity		#get the angle around the circle
			distance = random.normal(size, size/5)	#get a random distance based around a normal distribution
			point = [distance*math.sin(angle), distance*math.cos(angle)]
			points.append(point)
		self.track = points

	def saveTrack(self, filename):
		fileHandle = open(filename, 'w')
		pickle.dump(fileHandle)


if __name__ == "__main__":
	track = Track()
	track.generateTrack(20)
	print(track.track)
	import pygame
	pygame.init()
	window = pygame.display.set_mode((640, 480)) 
	for i in range(len(track.track)):
		if i == (len(track.track)-1):
			z = 0
		else:
			z = i+1
		pygame.draw.line(window, (255,255,255), (track.track[i][0]+100, track.track[i][1]+100), (track.track[z][0]+100, track.track[z][1]+100))
	pygame.display.flip()
	while True: 
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				sys.exit(0)

