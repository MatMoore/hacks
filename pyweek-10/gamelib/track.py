import constants
import pickle
import math
from numpy import *

class Track:
	def __init__(self, loadTrack = None):
		if loadTrack:
			fileHandle = open(loadTrack, 'r')
			self.track = pickle.load(fileHandle)
			self.makeOutsideTrack()

	def lineLineIntersection(self, p1, p2, p3, p4, segment = False):
		#from http://local.wasp.uwa.edu.au/~pbourke/geometry/lineline2d/
		denom = (p4[1] - p3[1]) * (p2[0] - p1[0]) - (p4[0] - p3[0]) * (p2[1] - p1[1])
		if denom == 0:	
			return array([False])															#if the denom is 0 it means the lines are parallel so return this and we can check for the case
		numer1 = (p4[0] - p3[0]) * (p1[1] - p3[1]) - (p4[1] - p3[1]) * (p1[0] - p3[0])
		m1 = numer1/denom
		x = p1[0] + m1*(p2[0]-p1[0])
		y = p1[1] + m1*(p2[1]-p1[1])
		if segment:
			#for segment calculation both m1 and m2 must be between 0 and 1
			if m1 >= 0 and m1 <= 1:
				numer2 = (p2[0] - p1[0]) * (p1[1] - p3[1]) - (p2[1] - p1[1]) * (p1[0] - p3[0])		#we onyl need to do this part if we are doing segment-segment checking
				m2 = numer2/denom
				if not (m2 >= 0 and m2 <= 1):
					return array([False])
			else:
				return array([False])

		return array([x,y])

	def makeOutsideTrack(self):
		self.quadPoints = []			#this is an openGl specific thing for how to draw the but i think it's better to store here than in the camera and def. better than generating it each frame
		self.outsideTrack = []
		for i in range(len(self.track)):
			if i == len(self.track)-1:	#if i is at the end then:
				p3 = self.track[0]		#get the first point
			else:
				p3 = self.track[i+1]
			p1 = self.track[i-1]	#this works because [-1] index will give last result
			p2 = self.track[i]
			#we now have p1, p2 and p3 which make 2 lines. we are calculating the outside point at p2
			#get the vectors for both lines
			dp12 = p2-p1
			dp23 = p3-p2
			
			# get the normal unit vector for both lines
			n1 = array([dp12[1]*-1, dp12[0]])
			n1 = n1 / linalg.norm(n1)
			n2 = array([dp23[1]*-1, dp23[0]])
			n2 = n2 / linalg.norm(n2)
			
			#now use the normal vector to shift both lines outwards
			iP1 = p1 + n1*constants.roadWidth
			iP2 = p2 + n1*constants.roadWidth
			iP3 = p2 + n2*constants.roadWidth
			iP4 = p3 + n2*constants.roadWidth
			
			#the above 4 points refer to the 2 outer lines that make the angle, now we need to find the intersection, to find the inside point
			#insidePoint = geometry.getIntersectPoint(iP1, iP2, iP3, iP4)
			point = self.lineLineIntersection(iP1, iP2, iP3, iP4)
			
			if point.all() == False:
				point = iP2			#it returns false if the lines are parallel (which could potentially happen) so here we set it to the point in the middle(either iP2 or iP3, should be the same)
				
			self.outsideTrack.append(point)
			self.quadPoints.append(self.track[i])
			self.quadPoints.append(point)

		#these last two just join it back up to the beginning
		self.quadPoints.append(self.track[0])
		self.quadPoints.append(self.outsideTrack[0])
		self.startingPoint = ((self.track[0][0] + self.outsideTrack[0][0])/2, (self.track[0][1] + self.outsideTrack[0][1])/2)
		self.startingVect = (self.track[1][0] - self.track[0][0], self.track[1][1] - self.track[0][1])
		self.startingRot = math.atan2(self.startingVect[1], self.startingVect[0])

	def generateTrack(self, complexity = 10, size = 50):		#complexity defines the number of points for the track, size = the average distance from the center of the map.
		points = []
		inside = []
		for i in range(complexity):
			angle = 2*math.pi * i/complexity		#get the angle around the circle
			distance = random.normal(size, size/5)	#get a random distance based around a normal distribution
			point = array([distance*math.sin(angle), distance*math.cos(angle)])
			points.append(point)
		self.track = points
		self.makeOutsideTrack()

	def saveTrack(self, filename):
		fileHandle = open(filename, 'w')
		pickle.dump(self.track, fileHandle)

	def isInsidePoly(self, position, polygon):
		#make two points at far left and right offset in the x direction, this gives two points on a horizontal line
		#these are clearly magic numbers and may need to be increased to stretch the segment out further
		#i'm also modifying the Y position up on one side and down on the other, this puts a slight tilt to it and avoids problems where we're directly on a horizontal node
		#there are better solutions here: http://alienryderflex.com/polygon/ but this is a quick hack that probably covers us
		
		p1 = (position[0]-10000, position[1]-500)
		p2 = (position[0]+10000, position[1]+500)
		
		intersectionsLeft = 0
		#Its a fairly simple algorithm, you take the intersections of a single line raycasted from the point and then determine if theres an odd number on each side, or an even number
		#if it's odd then you're inside the polygon, if it's even(or 0) then you're outside. We're only checking the left hand side, since you only need to check one side
		for i in range(len(polygon)):
			if i == len(polygon)-1:	#handle the last element in the list
				i2 = 0
			else:
				i2 = i+1
			intersection = self.lineLineIntersection(p1, p2, polygon[i], polygon[i2], True)	#the true on the end makes this segment-segment intersection
			if intersection.all() != False:
				if intersection[0] < position[0]:
					intersectionsLeft += 1
		if (intersectionsLeft % 2) == 1:	#if not divisible by 2(odd)
			return True						#then we're inside the poly
		else:
			return False

	def getFriction(self, position):				#position is just a 2d coordinate x, y, to determine if a point is on the track or off the track(this can be extended to different types of track terrain)
		#it needs to be inside the outer track and outside the inside track
		if (self.isInsidePoly((position[0], position[2]), self.outsideTrack) and not self.isInsidePoly((position[0], position[2]), self.track)):
			#it is on the track
			return constants.TRACKFRICTION
		else:
			return constants.GRASSFRICTION	#TODO: make a bunch of constants for terrain types


if __name__ == "__main__":
	track = Track()
	track.generateTrack(20,100)
	import pygame
	pygame.init()
	window = pygame.display.set_mode((640, 640)) 
	for i in range(len(track.track)):
		if i == (len(track.track)-1):
			z = 0
		else:
			z = i+1
		pygame.draw.line(window, (255,255,255), (track.track[i][0]*2+300, track.track[i][1]*2+300), (track.track[z][0]*2+300, track.track[z][1]*2+300))
		pygame.draw.line(window, (255,0,0), (track.outsideTrack[i][0]*2+300, track.outsideTrack[i][1]*2+300), (track.outsideTrack[z][0]*2+300, track.outsideTrack[z][1]*2+300))		
	pygame.display.flip()
	while True: 
		pygame.time.wait(50)
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				point = event.pos
				point = ((point[0]-300)/2, (point[1]-300)/2)	#convert it back into terrain coordinates
				print track.getTerrain(point)
