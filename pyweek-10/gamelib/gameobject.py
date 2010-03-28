from constants import *
from numpy import *

class GameObject
	def __init__(physicsTimeStep):
		self._position = array([0.0, 0.0, 0.0])
		self._positionOld = array([0.0, 0.0, 0.0])
		self._orientation = array([0.0, 0.0, 0.0])	#these might be really bad defaults
		self._orientationOld = array([0.0, 0.0, 0.0])
		self.timeSinceUpdate = 0


	def update():
		pass
		
	def interpolate(self, newVal, oldVal)
		return newVal + (newVal-oldVal)*self.timeSinceUpdate

	@property
	def position
		return self.interpolate(self._position, self._positionOld)
		
	@property
	def orientation
		return self.interpolate(self._orientation, self._orientationOld)
