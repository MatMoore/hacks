import constants
import camera
import track
import pygame
import math
import misc

class Game:
	def __init__(self):
		self.camera = camera.Camera()
		self.track = track.Track()
		self.track.generateTrack(20,50)
		self.camera.position = (self.track.startingPoint[0], 3, self.track.startingPoint[1])
	def main(self):
		self.camera.clear()
		self.camera.drawGround()
		self.camera.drawTrack(self.track)
		self.camera.drawPyramid()
		self.camera.flip()
		pygame.time.wait(50)
		

		
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
			newposX = pos[0] + 0.2*math.sin(ang)
			newposY = pos[2] + 0.2*math.cos(ang)			
			self.camera.position = (newposX, self.camera.position[1], newposY)
		if keys[pygame.K_DOWN]:
			pos = self.camera.position
			ang = misc.degToRad(180-self.camera.orientation[1])
			newposX = pos[0] - 0.2*math.sin(ang)
			newposY = pos[2] - 0.2*math.cos(ang)			
			self.camera.position = (newposX, self.camera.position[1], newposY)
		return constants.gsInGame
