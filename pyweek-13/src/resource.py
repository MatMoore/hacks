import os
import sys
import pygame
from logging import info,debug,error
from util import memoize

def data_path():
	return os.path.join(script_dir(), 'data')

def file_path(filename):
	return os.path.join(data_path(), filename)

def script_dir():
	return os.path.abspath(os.path.dirname(sys.argv[0]))

@memoize
def load_image(filename):
	return pygame.image.load(file_path(filename)).convert_alpha()
