import constants
import camera
import track
import pygame
import math
import misc
import racer
from numpy import *

class Game:
	def __init__(self):
		self.camera = camera.Camera()
		self.track = track.Track()
		self.track.generateTrack(20,50)
		self.camera.position = (self.track.startingPoint[0], 1, self.track.startingPoint[1])
		self.rotation = 0
		self.unicycles = []
		self.unicycles.append(racer.Unicycle(array([2,0.3,2]), array([0,1,0]), 0))
		self.unicycles.append(racer.Unicycle(array([-2,0.3,2]), array([0,0,1]), math.pi/2))
		self.unicycles.append(racer.Unicycle(array([2,0.3,-2]), array([0,1,0]), math.pi))
		self.unicycles.append(racer.Unicycle(array([-2,0.3,-2]), array([0,1,0]), 1.5*math.pi))
		self.unicycles.append(racer.Unicycle(array([0,0.3,2]), array([1,0,0]), math.pi*0.75))
		self.unicycles.append(racer.Unicycle(array([-2,0.3,0]), array([1,0,0]), 1.3*math.pi))
		self.unicycles.append(racer.Unicycle(array([0,0.3,-2]), array([0,0,1]), math.pi))
		self.unicycles.append(racer.Unicycle(array([2,0.3,0]), array([0,0,1]), 1.5*math.pi))
	def main(self):
		self.camera.clear()
		self.camera.drawSky()
		#self.camera.drawGround()
		self.camera.drawTrack(self.track)
		self.camera.drawPyramid()
		self.rotation += 3
		self.tilt = 20 * math.sin(self.rotation/100.0)
#		self.camera.drawUnicycle((self.track.startingPoint[0], 0.3, self.track.startingPoint[1]), (self.tilt,0,self.rotation))	#puts a unicycle at the start, the 0.3 hopefully moves it up out of the ground, since the wheel is 0.6 (60cm) around
		for unicycle in self.unicycles:
			self.camera.drawUnicycle(unicycle)
		self.camera.flip()
		pygame.time.wait(20)
		

		
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				return constants.gsQuit


		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.camera.orientation = (self.camera.orientation[0], self.camera.orientation[1]-1, self.camera.orientation[2])
		if keys[pygame.K_RIGHT]:
			self.camera.orientation = (self.camera.orientation[0], self.camera.orientation[1]+1, self.camera.orientation[2])
		if keys[pygame.K_UP]:
			pos = self.camera.position
			ang = misc.degToRad(180-self.camera.orientation[1])
			newposX = pos[0] + 0.5*math.sin(ang)
			newposY = pos[2] + 0.5*math.cos(ang)			
			self.camera.position = (newposX, self.camera.position[1], newposY)
		if keys[pygame.K_DOWN]:
			pos = self.camera.position
			ang = misc.degToRad(180-self.camera.orientation[1])
			newposX = pos[0] - 0.5*math.sin(ang)
			newposY = pos[2] - 0.5*math.cos(ang)			
			self.camera.position = (newposX, self.camera.position[1], newposY)
		if keys[pygame.K_a]:
			self.camera.position = (self.camera.position[0], self.camera.position[1] + 0.5, self.camera.position[2])
		if keys[pygame.K_z]:
			self.camera.position = (self.camera.position[0], self.camera.position[1] - 0.5, self.camera.position[2])
		return constants.gsInGame
