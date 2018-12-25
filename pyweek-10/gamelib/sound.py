import pygame
import data
import random
class Sound:
	def __init__(self):
		pygame.mixer.init()
		self.grunts = []
		for i in range(12):
			filename = "grunt"+str(i+1)+".wav"
			self.grunts.append(pygame.mixer.Sound(data.filepath("sounds/"+filename)))
		pygame.mixer.music.load(data.filepath("music/unicyclingFade.ogg"))
		pygame.mixer.music.play(-1) 
		
	def grunt(self):
		sound = random.choice(self.grunts)
		sound.play()
