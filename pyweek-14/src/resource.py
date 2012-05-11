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

def levels():
	return json.load(open(file_path('levels.json'), 'r'))
