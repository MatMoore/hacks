# If this class doesn't make sense to you don't worry, it doesn't make sense to me either.
from constants import *
from numpy import *
from gameobject import GameObject
from utils import *
import pygame

class Racer:
	def __init__(self,position,facing,mass=75,height=1.0, track=None):
#		self.height = height
		self.unicycle = Unicycle(position, facing, track)
		self.rider = Rider(position + array([0,UNICYCLE_HEIGHT,0]), facing, mass, height)
		self.unicycle.thetaFB = 0
		self.rider.thetaFB = 0
		self.autoBalanceAcc = 0

	def reset(self):
		self.rider._position = self.unicycle._position + array([0,UNICYCLE_HEIGHT,0])
		self.unicycle.thetaFB = 0
		self.unicycle.thetaLR = 0
		self.rider.thetaFB = 0
		self.rider.thetaLR = 0
		self.unicycle.isFallen = False
		self.unicycle.velocity = array([0,0,0])
		self.unicycle.angularVel = 0
		self.unicycle.angularAcc = 0
		self.rider.velocity = array([0,0,0])

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
		if self.unicycle.isFallen:
			self.rider.move()
			if pygame.time.get_ticks() - self.timeFallen > 1000:
				self.reset()
			return


		if self.unicycle.isFallenOver():
			self.rider.velocity = self.unicycle.velocity.copy()
			self.timeFallen = pygame.time.get_ticks()
			return
			

		# Base class update stuff
		GameObject.update(self.unicycle)
		GameObject.update(self.rider)

		self.wobble()

		# Adjust the acceleration to match the angle
		self.autoBalance()

		# update unicycle position using wheel accn
		self.unicycle.move()

		# update rider position by sticking him back on the top of the unicycle
		self.rider._position = self.unicycle.position + self.unicycle.orientation / linalg.norm(self.unicycle.orientation) * UNICYCLE_HEIGHT

	@property
	def height(self):
		return UNICYCLE_HEIGHT + 0.5 * self.rider.height

	def wobble(self):
		if not FALL_FORWARDS:
			return

		# Ok, our rider is now a perfect sphere sitting on a massless stick. DO NOT QUESTION THIS.
		#     o   <-- rider's mass
		#      \
		#       \  <-- uncicyle/human hybrid
		#        \
		#         O <-- wheel

		# Calculate vector from wheel to rider
		stickVector = self.unicycle.orientation * UNICYCLE_HEIGHT + 0.5 * self.rider.height * self.rider.orientation

		stickVectorRight = self.unicycle.rightYProjection(stickVector)
		
		# Project that into the forward-y plane
		stickVector = self.unicycle.forwardYProjection(stickVector)

		# Get current angle of the stick from vetical
		#     o
		#     :\
		#     :t\
		#     :--\
		#     :   O
		theta = angleBetween(stickVector, y)
		theta2 = angleBetween(stickVectorRight, y)
		rotated = dot(y, rotationMatrix(self.unicycle.right, theta))
		if (theta != 0) and not angleBetween(rotated, stickVector) < 0.01:
			# Rotating y forward gets to projection
			theta *= -1
		rotated = dot(y, rotationMatrix(self.unicycle.forward, theta2))
		if (theta2 != 0) and not angleBetween(rotated, stickVectorRight) < 0.01:
			# Rotating y forward gets to projection
			theta2 *= -1
		# Now we will attempt to calculate the new angle of the system. Assuming that the unicycle will rotate due to a) acceleration of the wheel and b) torque due to the riders COM
		self.unicycle.turnLeft(theta2*0.05)
		self.rider.turnLeft(theta2*0.05)		

		# Equation of motion (THIS IS PROBABLY WRONG):
		# mL^2 alpha = m L sin theta - M a L cos theta
		# L alpha = g sin theta - M/m a cos theta
		# L alpha = g sin theta - CONST a cost theta
		# where alpha is angular acceleration of stickvector, theta is angle of stickvector relative to the vertical, L is the length of the stick vector, g is graviation acceleration and a is wheel acceleration
		alphaOld = self.unicycle.angularAcc
		self.unicycle.angularAcc = 0.5*g * sin(theta) - UNICYCLE_MASS / self.rider.mass *self.unicycle.acceleration * cos(theta)
		#print alpha

		# integrate to get new angle
		#print "angularvel = %s" % self.unicycle.angularVel
		newTheta, newAngularVel = leapfrog(theta,self.unicycle.angularVel,self.unicycle.angularAcc, alphaOld)
		dtheta = newTheta - theta
		#print "Theta = %s, a=%s, alpha = %s, newAngularVel=%s, dtheta=%s" %(theta,self.unicycle.acceleration,alpha,newAngularVel,dtheta)

		# Ok lets work out what the actual unicycle angle would be to make this sphereonstick angle. Btw I am assuming rider is not wibbly wobbly indepent of the uni.
		
		# update unicycle orientation
		self.unicycle.angularVel = newAngularVel
		self.unicycle.thetaFB += dtheta

		#print 'unicycle angular vel is now %s, thetaFB is %s' % (self.unicycle.angularVel, self.unicycle.thetaFB)
		#print 'orientation='+str(self.unicycle.orientation)

	def autoBalance(self):
		if not AUTOBALANCE_ENABLED:
			return

		self.autoBalanceAcc = AUTOBALANCE_AMOUNT * -1 * self.unicycle.angularVel / self.height

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
		self.isFallen = False
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
		self._orientation = dot(self.orientation, rotationMatrix(y,angle))

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
		projection = self.rightYProjection(self.orientation)
		angle = angleBetween(projection, y)
		if (angle != 0) and angleBetween(dot(y, rotationMatrix(self.forward, angle)), projection) < 0.01:
			# Rotating y right gets to projection
			return angle
		else:
			return -angle


	@thetaLR.setter
	def thetaLR(self, value):
		'''Rotate around the forward vector'''

		# Go back to vertical
		self._orientation = dot(self.orientation, rotationMatrix(self.forward, -self.thetaLR))

		# Rotate to new angle
		self._orientation = dot(self.orientation, rotationMatrix(self.forward, value))

	@property
	def thetaFB(self):
		projection = self.forwardYProjection(self.orientation)
		angle = angleBetween(projection, y)
		if (angle != 0) and angleBetween(dot(y, rotationMatrix(self.right, angle)), projection) < 0.01:
			# Rotating y forward gets to projection
			return angle
		else:
			return -angle

	@thetaFB.setter
	def thetaFB(self, value):
		'''Rotate around the left vector'''
		# Go back to vertical
		self._orientation = dot(self.orientation, rotationMatrix(self.right, -self.thetaFB))

		# Rotate to new angle
		self._orientation = dot(self.orientation, rotationMatrix(self.right, value))

	def isFallenOver(self):
		flag = False
		if self.thetaFB > pi/2:
			self.thetaFB = pi/2
			flag = True
		elif self.thetaFB < -pi/2:
			self.thetaFB = -pi/2
			flag = True
		if self.thetaLR > pi/2:
			self.thetaLR = pi/2
			flag = True
		elif self.thetaLR < -pi/2:
			self.thetaLR = -pi/2
			flag = True
		if flag == True:
			self.isFallen = True
		return flag

class Rider(WibblyWobbly):
	def __init__(self, position, facing, mass, height):
		self.mass = mass
		self.height = height
		orientation = array([0, 1, 0]) # Start upright
		self.forward = dot(array([1,0,0]), rotationMatrix(array([0,1,0]), facing))
		self.velocity = array([0,0,0])
		GameObject.__init__(self, position,orientation,facing)

	def lean(self,dThetaLR, dThetaFB):
		if linalg.norm(self.velocity) == 0:		
			self.thetaLR += dThetaLR
			self.thetaFB += dThetaFB

	def move(self):
		self.velocity *= array([1,0,1])
		newPos, newVel = integrate(self.position, self.velocity, -self.velocity)
		self._position = newPos
		self.velocity = newVel * array([1,0,1])

class Unicycle(WibblyWobbly):
	def __init__(self,position, facing=0, track=None):
		self.velocity = array([0,0,0]) # wheel speed
		self.acceleration = 0 # wheel acceleration
		self.angularVel = 0 # angular velocity of frame
		self.angularAcc = 0
		self.track = track
		WibblyWobbly.__init__(self,position,facing)

	def move(self):
		'''Apply the wheel acceleration'''
		friction = 0
		if self.track != None:
			friction = -self.velocity * self.track.getFriction(self._position)
			angle = angleBetween(self.forward, self.velocity)
			friction = friction * (angle+1) * (angle+1)
			print friction
		

		
		newPos, newVel = integrate(self.position, self.velocity, self.forward*self.acceleration + friction)
		self._position = newPos
		self.velocity = newVel

if __name__ == "__main__":
	unicycle = Unicycle(array([0,0,0]), 0)
	print 'positive:'
	print unicycle.thetaFB
	unicycle.thetaFB = math.pi*0.25
	print unicycle.thetaFB
	print unicycle._orientation
	print unicycle.forwardYProjection(unicycle.orientation)
	print 'negative:'
	print unicycle.thetaFB
	unicycle.thetaFB = -math.pi*0.25
	print unicycle.thetaFB
	print unicycle._orientation
	print unicycle.forwardYProjection(unicycle.orientation)
	print 'sideways'
#	unicycle = Unicycle(array([0,0,0]), 0)
	print unicycle.thetaLR
	print 'positive:'
	unicycle.thetaLR = math.pi*0.25
	print unicycle.thetaLR

	print 'negative:'
	unicycle.thetaLR = -math.pi*0.25
	print unicycle.thetaLR
