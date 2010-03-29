from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import math

class Camera:
	def __init__(self, resX = 800, resY = 600):
		video_flags = OPENGL|DOUBLEBUF
		pygame.init()
		pygame.display.set_mode((resX, resY), video_flags)
		glViewport(0, 0, resX, resY)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45, 1.0*resX/resY, 0.1, 100.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glShadeModel(GL_SMOOTH)
		glClearColor(0.0, 0.0, 0.0, 0.0)
		glClearDepth(1.0)
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)
		glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
		self.rotationY = 0	#rotation around the Y axis, all i'm concerned with right now


	def drawTrack(self, track):
		glTranslatef(0.0, -10, 0.0)
		glRotatef(self.rotationY,0,1,0)
		glBegin(GL_QUAD_STRIP)
		for point in track.quadPoints:
			glVertex3f(point[0], 0, point[1])
		glEnd()

	def clear(self):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()

	def flip(self):
		pygame.display.flip()
