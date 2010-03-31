import constants
import camera
import track
import pygame
import math
import misc
import racer
import gameobject
from utils import *
from numpy import *

class Game:
	def __init__(self):
		self.camera = camera.Camera()
		self.track = track.Track()
		self.track.generateTrack(20,50)
		#self.camera.position = (self.track.startingPoint[0], 1, self.track.startingPoint[1])
		self.rotation = 0
		self.unicycles = []
		self.unicycles.append(racer.Unicycle(array([2,0.3,2]), 0))
		tilted = racer.Unicycle(array([-2,0.3,2]), 0)
		tilted.orientation = array([1, 1, 0])
		self.unicycles.append(tilted)
		
		tilted2 = racer.Unicycle(array([2,0.3,-2]), 0)
		tilted2.orientation = array([0, 1, 1])
		self.unicycles.append(tilted2)
		
		tilted3 = racer.Unicycle(array([-2,0.3,-2]), 0)
		tilted3.orientation = array([1, 1, 1])
		self.unicycles.append(tilted3)
		
		self.currentTime = pygame.time.get_ticks()
		self.accumulator = 0
#		self.unicycles.append(racer.Unicycle(array([-2,0.3,2]), array([0,0,1]), math.pi/2))
#		self.unicycles.append(racer.Unicycle(array([2,0.3,-2]), array([0,1,0]), math.pi))
#		self.unicycles.append(racer.Unicycle(array([-2,0.3,-2]), array([0,1,0]), 1.5*math.pi))
#		self.unicycles.append(racer.Unicycle(array([0,0.3,2]), array([1,0,0]), math.pi*0.75))
#		self.unicycles.append(racer.Unicycle(array([-2,0.3,0]), array([1,0,0]), 1.3*math.pi))
#		self.unicycles.append(racer.Unicycle(array([0,0.3,-2]), array([0,0,1]), math.pi))
#		self.unicycles.append(racer.Unicycle(array([2,0.3,0]), array([0,0,1]), 1.5*math.pi))

	def processInput(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.camera.orientation = (self.camera.orientation[0], self.camera.orientation[1]-3, self.camera.orientation[2])
		if keys[pygame.K_RIGHT]:
			self.camera.orientation = (self.camera.orientation[0], self.camera.orientation[1]+3, self.camera.orientation[2])
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
			self.camera.position = (self.camera.position[0], self.camera.position[1] + 0.4, self.camera.position[2])
		if keys[pygame.K_z]:
			self.camera.position = (self.camera.position[0], self.camera.position[1] - 0.4, self.camera.position[2])
		
		if keys[pygame.K_w]:
			self.unicycles[0].speed = 1
		elif keys[pygame.K_s]:
			self.unicycles[0].speed = -1
		else:
			self.unicycles[0].speed = 0
		self.unicycles[0].move()

	def update(self):
		for unicycle in self.unicycles:
			unicycle.turnRight(pi/200)
			# Rotate about y axis
			#unicycle.forward = dot(unicycle.forward, rotationMatrix(y, pi/200))


	def render(self):
		self.camera.clear()
		self.camera.drawSky()
		self.camera.drawGround()
		self.camera.drawTrack(self.track)
		self.rotation += 3
		self.tilt = 20 * math.sin(self.rotation/100.0)
		for unicycle in self.unicycles:
			self.camera.drawUnicycle(unicycle)
		self.camera.flip()

	def main(self):
		newTime = pygame.time.get_ticks()
		dt = (newTime - self.currentTime)/1000.0
		self.currentTime = newTime
		#pygame.time.wait(10)
		self.accumulator += dt
		while self.accumulator >= constants.TIMESTEP:
			self.processInput()
			self.update()
			self.accumulator -= constants.TIMESTEP

		gameobject.GameObject.timeSinceUpdate = self.accumulator	#set the timeSinceLastUpdate so that the interpolation on the objects will work
		self.render()


		#handles closing the window (not done in input because we want to return gsQuit, it's clearer this way)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return constants.gsQuit

		return constants.gsInGame
