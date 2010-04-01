from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import math
import constants
import misc
import objloader
import data
import racer
from utils import *
from numpy import *

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
		glEnable(GL_TEXTURE_2D);
		self.loadTextures()
		glShadeModel(GL_SMOOTH)
		glClearColor(.5,.5,1,0)
		glClearDepth(1.0)
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)
		glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
		self.loadObjects()
		self.orientation = (0,-90,0) 	#current orientation
		self.position = (0,1,0)		#current position
		self.tempY = 0.01
		self.quadratic = gluNewQuadric()
		gluQuadricTexture(self.quadratic, True)


	def follow(self, racer):
		unicycle = racer.unicycle
		self.following = racer
		self.position = unicycle.position - (unicycle.forward * constants.viewDistanceBack) + (unicycle.right * constants.viewDistanceRight)
		self.position += array([0,constants.viewDistanceUp,0])
		self.orientation = array([0,misc.radToDeg(atan2(unicycle.forward[0],unicycle.forward[2])) + 90,0])
		self.lookDownAngle = misc.radToDeg(math.atan2(constants.viewDistanceUp, constants.viewDistanceBack)) + constants.lookAngleAdjust

	def loadObjects(self):
		self.objects = {}
		self.objects['wheel'] = objloader.OBJ("wheel.obj")
		self.objects['frame'] = objloader.OBJ("frame.obj")
		
	def loadTexture(self, filename, name):
		texturefile = data.filepath(filename)
		textureSurface = pygame.image.load(texturefile)
		textureData = pygame.image.tostring(textureSurface, "RGBX", 1)
		self.textures[name] = self.textureNum
		self.textureNum += 1	#we need a unique number for each texture.
		glBindTexture(GL_TEXTURE_2D, self.textures[name])
		glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData );
#		glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE );		
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

	def loadTextures(self):
		self.textures = {}
		self.textureNum = 0
		self.loadTexture('grass.png', 'grass')
		self.loadTexture('sky.jpg', 'sky')

	def resetForNextObject(self):
		glLoadIdentity()

	def translateForCameraCoords(self, position):
		glTranslatef(position[0]-self.position[0], position[1]-self.position[1], position[2]-self.position[2])

	def rotateForObjectRotation(self, orientation):
		glRotatef(orientation[0],1,0,0)
		glRotatef(orientation[1],0,1,0)
		glRotatef(orientation[2],0,0,1)

	def rotateForCameraRotation(self):
		glRotatef(270-self.orientation[1], 0, 1, 0)
		glRotatef(self.lookDownAngle, self.following.unicycle.right[0], self.following.unicycle.right[1], self.following.unicycle.right[2])


	def drawGround(self):
		glEnable(GL_TEXTURE_2D);
		self.rotateForCameraRotation()		#the ground plane is not rotated
		self.translateForCameraCoords((0,-0.01,0))	#we do lower it ever so slightly though, this is so the track can go on 0,0,0 without any possible interference
		self.rotateForObjectRotation((0,0,0))
		glColor3f(0.2,0.4,0.2)							#it should be green
		glBindTexture(GL_TEXTURE_2D, self.textures['grass'])
		glBegin(GL_QUADS)							#draw a big quad for the grass
		glTexCoord2f(0, 0)
		glVertex3f(-200,0,-200)
		glTexCoord2f(0.0, 50.0)
		glVertex3f(-200,0,200)
		glTexCoord2f(50.0, 50.0)
		glVertex3f(200,0,200)
		glTexCoord2f(50.0, 0.0)
		glVertex3f(200,0,-200)
		glEnd()
		glDisable(GL_TEXTURE_2D)
		self.resetForNextObject()

	def drawSky(self):
		self.rotateForCameraRotation()
		self.rotateForObjectRotation((90,0,90))
		glColor4f(1,1,1,1)
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, self.textures['sky'])
		gluSphere(self.quadratic,300,20,20)
		glDisable(GL_TEXTURE_2D)
		self.resetForNextObject()

	def drawTrack(self, track):
		self.rotateForCameraRotation()	
		self.translateForCameraCoords((0,0,0))		#center of track is at 0,0,0
		self.rotateForObjectRotation((0,0,0))		#track doesnt need rotating
		glColor3f(0.4,0.4,0.4)						#make it grey
		glBegin(GL_QUAD_STRIP)
		for point in track.quadPoints:
			glVertex3f(point[0], 0, point[1])
		glEnd()
		self.resetForNextObject()

	def drawRider(self, racer):
		rider = racer.rider
		glDisable(GL_TEXTURE_2D)
		self.rotateForCameraRotation()
		self.translateForCameraCoords(rider.position)

		vec = rider.orientation * rider.height
		glColor3f(1,1,1)
		glBegin(GL_LINES)
		glVertex3f(0,0,0)
		glVertex3f(vec[0], vec[1], vec[2])
		glEnd()
		self.resetForNextObject()

	def drawUnicycle(self, racer):
		unicycle = racer.unicycle
		glDisable(GL_TEXTURE_2D)
		self.rotateForCameraRotation()
		self.translateForCameraCoords(unicycle.position)
		#glRotatef(misc.radToDeg(unicycle.rotation), unicycle.orientation[0], unicycle.orientation[1], unicycle.orientation[2])

		vec = unicycle.forwardYProjection(unicycle.orientation)
		glColor3f(1,1,0)
		glBegin(GL_LINES)
		glVertex3f(0,0,0)
		glVertex3f(vec[0], vec[1], vec[2])
		glEnd()

		vec = unicycle.rightYProjection(unicycle.orientation)
		glColor3f(0,1,1)
		glBegin(GL_LINES)
		glVertex3f(0,0,0)
		glVertex3f(vec[0], vec[1], vec[2])
		glEnd()

		glColor3f(1,0,0)
		glBegin(GL_LINES)
		glVertex3f(0,0,0)
		glVertex3f(unicycle.forward[0], unicycle.forward[1], unicycle.forward[2])
		glEnd()

		glColor3f(0,1,0)
		glBegin(GL_LINES)
		glVertex3f(0,0,0)
		glVertex3f(unicycle.right[0], unicycle.right[1], unicycle.right[2])
		glEnd()

		glColor3f(0,0,1)
		glBegin(GL_LINES)
		glVertex3f(0,0,0)
		glVertex3f(unicycle.orientation[0], unicycle.orientation[1], unicycle.orientation[2])
		glEnd()
		
#		tiltLRAngle = misc.radToDeg(unicycle.thetaLR)
#		glRotatef(tiltLRAngle, unicycle.forward[0], unicycle.forward[1], unicycle.forward[2])

#		tiltFBAngle = misc.radToDeg(unicycle.thetaFB)
#		glRotatef(tiltFBAngle, unicycle.left[0], unicycle.left[1], unicycle.left[2])	

		normal = cross(unicycle.orientation, y)
		glColor3f(0,0,0)
		glBegin(GL_LINES)
		glVertex3f(0,0,0)
		glVertex3f(normal[0]*2, normal[1]*2, normal[2]*2)
		glEnd()
		normAng = -misc.radToDeg(angleBetween(unicycle.orientation, y))
		glRotatef(normAng, normal[0], normal[1], normal[2])
		
		uniAngle = misc.radToDeg(atan2(unicycle.forward[0],unicycle.forward[2])) + 90
		glRotatef(uniAngle, 0, 1, 0)
		
		glCallList(self.objects['wheel'].gl_list)
		glCallList(self.objects['frame'].gl_list)
		self.resetForNextObject()

	def clear(self):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()	#same as self.resetForNextObject

	def flip(self):
		pygame.display.flip()
