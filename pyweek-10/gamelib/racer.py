# If this class doesn't make sense to you don't worry, it doesn't make sense to me either.
from constants import *
from numpy import *
from gameobject import GameObject
from utils import *
from math import *
import pygame

class Racer:
	def __init__(self,position,facing,mass=75,height=1.0):
		self.height = height
		self.unicycle = Unicycle(position, facing)
		self.rider = Rider(position + array([0,UNICYCLE_HEIGHT,0]), facing, mass, height)

	def update(self):
		#         ahhh!
		#     o_   /
		#    _/\\
		#       \|
		#      /|~
		#     _\|_
		#      /
		#  ___O_____
		#

		# Base class update stuff
		GameObject.update(self.unicycle)
		GameObject.update(self.rider)

# TODO move this to input code (need to draw a rider first!)
		# Map mouse movement to rider (not uncycle) tilt
		#dthetaLR, dthetaFB = map((lambda x: max(pi / 2, x * TILT_ANGLE_PER_PIXEL_PER_SEC * TIMESTEP)), pygame.mouse.get_rel())

		# Update rider orientation
		#self.rider.lean(dthetaLR, dthetaFB)

		# Ok, our rider is now a perfect sphere sitting on a massless stick. DO NOT QUESTION THIS.
		#     o   <-- rider's mass
		#      \
		#       \  <-- uncicyle/human hybrid
		#        \
		#         O <-- wheel

		# Calculate vector from wheel to rider
		stickVector = self.unicycle.orientation * UNICYCLE_HEIGHT + 0.5 * self.rider.height * self.rider.orientation

		# Project that into the forward-y plane
		stickVector = self.unicycle.forwardYProjection(stickVector)

		# Get current angle of the stick from vetical
		#     o
		#     :\
		#     :t\
		#     :--\
		#     :   O
		theta = angleBetween(stickVector, y)

		# Now we will attempt to calculate the new angle of the system. Assuming that the unicycle will rotate due to a) acceleration of the wheel and b) torque due to the riders COM

		# Equation of motion (THIS IS PROBABLY WRONG):
		# mL^2 alpha = m L sin theta - M a L cos theta
		# L alpha = g sin theta - M/m a cos theta
		# L alpha = g sin theta - CONST a cost theta
		# where alpha is angular acceleration of stickvector, theta is angle of stickvector relative to the vertical, L is the length of the stick vector, g is graviation acceleration and a is wheel acceleration
		alpha = g * sin(theta) - UNICYCLE_MASS / self.rider.mass *self.unicycle.acceleration * cos(theta)

		# integrate to get new angle
		print "angularvel = %s" % self.unicycle.angularVel
		newTheta, newAngularVel = integrate(theta,self.unicycle.angularVel,alpha)
		dtheta = newTheta - theta
		print "Theta = %s, a=%s, alpha = %s, newAngularVel=%s, dtheta=%s" %(theta,self.unicycle.acceleration,alpha,newAngularVel,dtheta)

		# Ok lets work out what the actual unicycle angle would be to make this sphereonstick angle. Btw I am assuming rider is not wibbly wobbly indepent of the uni.
		
		# update unicycle orientation
		self.unicycle.angularVel = newAngularVel
		self.unicycle.thetaFB += dtheta
		print 'unicycle angular vel is now %s, thetaFB is %s' % (self.unicycle.angularVel, self.unicycle.thetaFB)
		print 'orientation='+str(self.unicycle.orientation)

		# update unicycle position using wheel accn
		self.unicycle.move()

		# update rider position by sticking him back on the top of the unicycle
		self.rider._position = self.unicycle.position + self.unicycle.orientation * UNICYCLE_HEIGHT


class WibblyWobbly(GameObject):
	'''Directions/angles:
	Forward,backward,left,right are all unit vectors in the X-Z plane, describing which way the unicycle wheel is moving
	Orientation is the "up" unit vector, and describes how the wobbly is tilted
thetaFB is the angle from vertical the left-up plane is rotated
thetaLR is the angle from vertical the forward-up plane is rotated
	'''
	def __init__(self, position, facing):

		orientation = array([0, 1, 0]) # Start upright

		# Work out the direction we're moving in
		# The unicycle starts vertical, so the "facing" angle is the angle from the x axis.
		self.forward = dot(array([1,0,0]), rotationMatrix(array([0,1,0]), facing))
		GameObject.__init__(self, position,orientation,facing)

	@property
	def left(self):
		return cross(y, self.forward)

	@property
	def right(self):
		return -self.left

	@property
	def backward(self):
		return -self.forward

	def turnRight(self, angle):
		self.forward = dot(self.forward, rotationMatrix(y, angle))
		self.orientation = dot(self.orientation, rotationMatrix(y,angle))

	def turnLeft(self, angle):
		self.turnRight(-angle)

	def forwardYProjection(self, vector):
		'''Return the component of the vector in the forward-Y plane'''
		# A || B = B x (AxB / |B|) / |B|
		# where A is vector B is normal to the plane
		normal = cross(self.forward, y)
		return cross(normal, (cross(vector,normal)/linalg.norm(normal))) / linalg.norm(normal)

	def rightYProjection(self, vector):
		'''Return the component of the vector orientation in the right-Y plane'''
		normal = cross(self.right, y)
		return cross(normal, (cross(vector,normal)/linalg.norm(normal))) / linalg.norm(normal)

	@property
	def thetaLR(self):
		rYP = self.rightYProjection(self.orientation)
		return atan2(fYP[1], fYP[0])
#		return angleBetween(self.rightYProjection(self.orientation), y)

	@thetaLR.setter
	def thetaLR(self, value):
		'''Rotate around the forward vector'''

		# Go back to vertical
		self._orientation = dot(self.orientation, rotationMatrix(self.forward, -self.thetaLR))

		# Rotate to new angle
		self._orientation = dot(self.orientation, rotationMatrix(self.forward, value))

	@property
	def thetaFB(self):
		fYP = self.forwardYProjection(self.orientation)
		return atan2(fYP[1], fYP[2])
#		return angleBetween(self.forwardYProjection(self.orientation), y)

	@thetaFB.setter
	def thetaFB(self, value):
		'''Rotate around the left vector'''
		# Go back to vertical
		self._orientation = dot(self.orientation, rotationMatrix(self.left, -self.thetaFB))

		# Rotate to new angle
		self._orientation = dot(self.orientation, rotationMatrix(self.left, value))


class Rider(WibblyWobbly):
	def __init__(self, position, facing, mass, height):
		self.mass = mass
		self.height = height
		orientation = array([0, 1, 0]) # Start upright
		self.forward = dot(array([1,0,0]), rotationMatrix(array([0,1,0]), facing))
		GameObject.__init__(self, position,orientation,facing)

	def lean(dThetaLR, dThetaFB):
		self.thetaLR += dThetaLR
		self.thetaFB += dThetaFB

class Unicycle(WibblyWobbly):
	def __init__(self,position, facing=0):
		self.speed = 0 # wheel speed
		self.acceleration = 0 # wheel acceleration
		self.angularVel = 0 # angular velocity of frame
		WibblyWobbly.__init__(self,position,facing)

	def move(self):
		'''Apply the wheel acceleration'''
		newPos, newVel = integrate(self.position, self.speed * self.forward, self.acceleration)
		newSpeed = dot(newVel,transpose(self.forward))
		self._position = newPos
		self.speed = newSpeed

if __name__ == "__main__":
	unicycle = Unicycle(array([0,0,0]), 0)
	print 'positive:'
	print unicycle.thetaFB
	unicycle.thetaFB = math.pi*0.25
	print unicycle.thetaFB
	print unicycle.orientation
	print unicycle.forwardYProjection(unicycle.orientation)
	print 'negative:'
	print unicycle.thetaFB
	unicycle.thetaFB = -math.pi*0.25
	print unicycle.thetaFB
	print unicycle.orientation
	print unicycle.forwardYProjection(unicycle.orientation)
