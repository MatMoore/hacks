'''Utility functions for loading game resources'''
import os
import sys
import pygame
import json

images = {}
fonts = {}

def data_path():
	'''data directory'''
	return os.path.join(script_dir(), 'data')

def file_path(filename):
	'''full path to a data file'''
	return os.path.join(data_path(), filename)

def script_dir():
	'''src path'''
	return os.path.abspath(os.path.dirname(sys.argv[0]))

def load_image(filename):
	'''load an image'''
	if filename not in images:
		images[filename] = pygame.image.load(os.path.join(data_path(), filename)).convert_alpha()
	return images[filename]

def load_font(filename, size):
	if (filename, size) not in fonts:
		path = os.path.join(data_path(), 'fonts', filename)
		fonts[(filename, size)] = pygame.font.Font(path, size)
	return fonts[(filename, size)]

sounds = {}
def load_sounds():
	from config import settings
	if not settings.getboolean('Sound', 'enabled'):
		return
	for filename in ('jetpack.wav', 'win.wav', 'WilhelmScream.ogg', 'powerup.wav', 'powerdown.wav'):
		path = file_path(filename)
		sounds[filename] = pygame.mixer.Sound(path)
	sounds['jetpack.wav'].set_volume(0.1)
	sounds['powerup.wav'].set_volume(0.8)
	sounds['powerdown.wav'].set_volume(0.4)

def levels():
	return json.load(open(file_path('levels.json'), 'r'))

def play_music():
	from config import settings
	if not settings.getboolean('Sound', 'enabled'):
		return
	pygame.mixer.music.load(file_path('DoKashiteru_-_The_Annual_New_England_Xylophone_Symposium.ogg'))
	pygame.mixer.music.play(-1)

def play_sound(name):
	try:
		sounds[name].play()
	except KeyError:
		pass
