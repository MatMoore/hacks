import constants
import pickle
import math
import geometry		#geometry.py file taken from http://www.pygame.org/wiki/IntersectingLineDetection
from numpy import *

class Track:
	def __init__(self, loadTrack = None):
		if loadTrack:
			fileHandle = open(loadTrack, 'r')
			self.track = pickle.load(fileHandle)
			self.makeQuads()

#	def lineLineIntersection(self, p1, p2, p3, p4):
#		#from http://local.wasp.uwa.edu.au/~pbourke/geometry/lineline2d/
#		numer1 = (p4[0] - p3[0]) * (p1[1] - p3[1]) - (p4[1] - p3[1]) * (p1[0] - p3[0])
#		numer2 = (p2[0] - p1[0]) * (p1[1] - p3[1]) - (p2[1] - p1[1]) * (p1[0] - p3[0])
#		denom = (p4[1] - p3[1]) * (p2[0] - p1[0]) - (p4[0] - p3[0]) * (p2[1] - p1[1])
#		if denom == 0:
#			return False
#		m1 = numer1/denom
#		m2 = numer2/denom
#		x = p1[0] + m1*(p2[0]-p1[0])
#		y = p1[1] + m2*(
#
#	def makeQuads(self):
#		self.inside = []
#		for i in range(len(self.track)):
#			if i == len(self.track)-1:	#if i is at the end then:
#				p3 = self.track[0]		#get the first point
#			else:
#				p3 = self.track[i+1]
#			p1 = self.track[i-1]	#this works because [-1] index will give last result
#			p2 = self.track[i]
#			#we now have p1, p2 and p3
#			dp12 = p2-p1
#			dp23 = p3-p2
#			n1 = array([dp12[1], dp12[0]])
#			n1 = n1 / linalg.norm(n1)
#			n2 = array([dp23[1], dp23[0]])
#			n2 = n2 / linalg.norm(n2)
#			print n1
#			print n2
#			iP1 = p1 + n1*constants.roadwidth/2
#			iP2 = p2 + n1*constants.roadwidth/2
#			iP3 = p2 + n2*constants.roadwidth/2
#			iP4 = p3 + n2*constants.roadwidth/2
#			#the above 4 points refer to the 2 inner lines that make the angle, now we need to find the intersection, to find the inside point
#			insidePoint = geometry.getIntersectPoint(iP1, iP2, iP3, iP4)
#			print insidePoint[0]
#			self.inside.append(insidePoint[0])


	def generateTrack(self, complexity = 10, size = 50):		#complexity defines the number of points for the track, size = the average distance from the center of the map.
		points = []
		inside = []
		for i in range(complexity):
			angle = 2*math.pi * i/complexity		#get the angle around the circle
			distance = random.normal(size, size/5)	#get a random distance based around a normal distribution
			point = array([distance*math.sin(angle), distance*math.cos(angle)])
			points.append(point)
			distance -= constants.roadwidth
			innerpoint = array([distance*math.sin(angle), distance*math.cos(angle)])
			inside.append(innerpoint)
		self.track = points
		self.inside = inside

	def saveTrack(self, filename):
		fileHandle = open(filename, 'w')
		pickle.dump(self.track, fileHandle)


if __name__ == "__main__":
	track = Track()
	track.generateTrack(12)
#	track.makeQuads()
	print(track.track)
	import pygame
	pygame.init()
	window = pygame.display.set_mode((640, 640)) 
	for i in range(len(track.track)):
		if i == (len(track.track)-1):
			z = 0
		else:
			z = i+1
		pygame.draw.line(window, (255,255,255), (track.track[i][0]*2+300, track.track[i][1]*2+300), (track.track[z][0]*2+300, track.track[z][1]*2+300))
	for i in range(len(track.inside)):
		if i == (len(track.inside)-1):
			z = 0
		else:
			z = i+1
		pygame.draw.line(window, (255,255,255), (track.inside[i][0]*2+300, track.inside[i][1]*2+300), (track.inside[z][0]*2+300, track.inside[z][1]*2+300))		
	pygame.display.flip()
	while True: 
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				sys.exit(0)

