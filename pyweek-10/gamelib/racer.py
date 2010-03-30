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
	def __init__(self,position,orientation, facing):
		self.wheelvelocity = array([0,0,0]) # velocity of the unicycle wheel (should be in the horizontal plane!)
		GameObject.__init__(position,orientation,facing)

	@property
	def self.forward(self):
		pass

	@property
	def thetaLR(self):
		'''Get the angle the unicycle is tilting around the forward vector'''
		return angleBetween(self.orientation,self.forward)

	@theraLR.setter
	def thetaLR(self, value):
		'''Set the angle the unicycle is tilting around the forward vector'''
		pass

	@property
	def thetaFB(self):
		'''Get the angle the unicycle is tilting in the forward backward direction'''
		return

	@theraFB.setter
	def thetaFB(self, value):
		'''Set the angle the unicycle is tilting in the forward backward direction'''
		pass
