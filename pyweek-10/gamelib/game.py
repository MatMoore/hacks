import constants
import camera
import track
import pygame

class Game:
	def __init__(self):
		self.camera = camera.Camera()
		self.track = track.Track()
		self.track.generateTrack(20,50)

	def main(self):
		self.camera.clear()
		self.camera.drawGround()
		self.camera.drawTrack(self.track)
		self.camera.flip()
		pygame.time.wait(50)
		
		self.camera.orientation = (self.camera.orientation[0], self.camera.orientation[1]+0.5, self.camera.orientation[2])	#just a quick hack to make something happen
		
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				return constants.gsQuit
		return constants.gsInGame
