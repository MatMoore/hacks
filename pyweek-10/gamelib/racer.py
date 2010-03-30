# If this class doesn't make sense to you don't worry, it doesn't make sense to me either.
from constants import *
from numpy import *
from gameobject import GameObject
import pygame

class Racer:
	def __init__(position,orientation,mass=75,height=1.0):
		self.height = height
		self.unicycle = GameObject()
		self.rider = GameObject()

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

		# Map mouse movement to rider (not uncycle) tilt
		dthetaLR, dthetaFB = map(lamda x: max(pi / 2, x * TILT_ANGLE_PER_PIXEL_PER_SEC * TIMESTEP), pygame.mouse.get_rel()
		# Update rider orientation
		self.rider.lean(dthetaLR, dthetaFB)

		# Ok, our rider is now a perfect sphere sitting on a massless stick. DO NOT QUESTION THIS.
		#     o   <-- rider's mass
		#      \
		#       \  <-- uncicyle/human hybrid
		#        \
		#         O <-- wheel

		# Calculate vector from wheel to rider
		stickVector = self.unicycle.orientation * UNICYCLE_HEIGHT + 0.5 * self.rider.height * self.rider.orientation

		# Get current angle of the stick from vetical
		#     o
		#     :\
		#     :t\
		#     :--\
		#     :   O

		# Now we will attempt to calculate the new angle of the system.

		# Equation of motion:
		# L alpha = g sin theta - a cos theta
		# where alpha is angular acceleration of stickvector, theta is angle of stickvector relative to the vertical, L is the length of the stick vector, g is graviation acceleration and a is wheel acceleration

		# integrate to get new angle

		# Ok lets work out what the actual unicycle angle would be to make this sphereonstick angle. Btw I am assuming rider is not wibbly wobbly indepent of the uni.

		# update unicycle orientation

		# update unicycle position using wheel accn
		
		# update rider position by sticking him back on the top of the unicycle

class Unicycle(GameObject):
	'''Unicycle directions/angles:
	Forward,backward,left,right are all unit vectors in the X-Z plane, describing which way the unicycle wheel is moving
	Orientation is the "up" unit vector, and describes how the unicycle is tilted
thetaFB is the angle from vertical the left-up plane is rotated
thetaLR is the angle from vertical the forward-up plane is rotated
	'''
	def __init__(self,position,orientation, facing):
		self.wheelvelocity = array([0,0,0]) # velocity of the unicycle wheel (should be in the horizontal plane!)

		# Work out the direction we're moving in
		# The unicycle starts vertical, so the "facing" angle is the angle from the x axis.
		self.forward = array([1,0,0]) * rotationMatrix(array([0,1,0]), facing)
		GameObject.__init__(position,orientation,facing)

	@property
	def left(self):
		cross(y, self.forward)

	@property
	def right(self):
		return -self.left

	@property
	def backward(self):
		return -self.forward

	@property
	def thetaLR(self):
		'''The angle between the forward-up unicycle plane and the y axis.'''
		# This is 90 deg - (angle between the normal and the y axis)
		normal = cross(self.forward, self.orientation)
		return  pi/2 - angleBetween(y, normal)

	@theraLR.setter
	def thetaLR(self, value):
		'''Rotate around the forward vector'''

		# Go back to vertical
		self.orientation *= rotationMatrix(self.forward, -self.thetaLR)

		# Rotate to new angle
		self.orientation *= rotationMatrix(self.forward, value)

	@property
	def thetaFB(self):
		'''The angle between the left-up unicycle plane and the y axis'''
		# This is 90 deg - (angle between the normal and the y axis)
		normal = cross(self.left, self.orientation)
		return  pi/2 - angleBetween(y, normal)

	@theraFB.setter
	def thetaFB(self, value):
		'''Rotate around the left vector'''

		# Go back to vertical
		self.orientation *= rotationMatrix(self.left, -self.thetaFB)

		# Rotate to new angle
		self.orientation *= rotationMatrix(self.left, value)


