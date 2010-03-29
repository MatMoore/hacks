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
		self.camera.drawTrack(self.track)
		self.camera.flip()
		pygame.time.wait(50)
		self.camera.rotationY += 1
		return constants.gsInGame
