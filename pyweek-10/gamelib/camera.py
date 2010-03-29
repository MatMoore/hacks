from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import math
import constants
import misc
import objloader
import data

class Camera:
	def __init__(self, resX = 800, resY = 600):
		video_flags = OPENGL|DOUBLEBUF
		pygame.init()
		pygame.display.set_mode((resX, resY), video_flags)
		glViewport(0, 0, resX, resY)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45, 1.0*resX/resY, 0.1, 300.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glShadeModel(GL_SMOOTH)
		glClearColor(0.0, 0.0, 0.0, 0.0)
		glClearDepth(1.0)
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)
		glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
		glClearColor(.5,.5,1,0)
		self.orientation = (0,-90,0) 	#current orientation
		self.position = (0,3,0)		#current position
		self.loadObjects()
		self.tempY = 0.01

	def loadObjects(self):
		self.objects = {}
		self.objects['pyramid'] = objloader.OBJ("pyramid.obj")


	def resetForNextObject(self):
		glLoadIdentity()

	def translateForCameraCoords(self, position):
		glTranslatef(position[0]-self.position[0], position[1]-self.position[1], position[2]-self.position[2])

	def rotateForCameraRotation(self, orientation):
		glRotatef(self.orientation[0]-orientation[0],1,0,0)
		glRotatef(self.orientation[1]-orientation[1],0,1,0)
		glRotatef(self.orientation[2]-orientation[2],0,0,1)

	def drawPyramid(self):
		self.tempY += 0.01
		self.rotateForCameraRotation((0,0,0))		#lets rotate it 45 degrees in the y axis
		self.translateForCameraCoords((0,3,0))		#stick it floating in the air in the middle of the track a bit
		glCallList(self.objects['pyramid'].gl_list)
		self.resetForNextObject()

	def drawGround(self):
		self.rotateForCameraRotation((0,0,0))		#the ground plane is not rotated
		self.translateForCameraCoords((0,-0.01,0))	#we do lower it ever so slightly though, this is so the track can go on 0,0,0 without any possible interference
		glColor3d(0,0.4,0)							#it should be green
		glBegin(GL_QUADS)							#draw a big quad for the grass
		glVertex3f(-200,0,200)
		glVertex3f(200,0,200)
		glVertex3f(200,0,-200)
		glVertex3f(-200,0,-200)
		glEnd()
		self.resetForNextObject()


	def drawTrack(self, track):
		self.rotateForCameraRotation((0,0,0))		#track doesnt need rotating
		self.translateForCameraCoords((0,0,0))		#center of track is at 0,0,0
		glColor3f(0.4,0.4,0.4)						#make it grey
		glBegin(GL_QUAD_STRIP)
		for point in track.quadPoints:
			glVertex3f(point[0], 0, point[1])
		glEnd()
		self.resetForNextObject()

	def clear(self):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()	#same as self.resetForNextObject

	def flip(self):
		pygame.display.flip()
