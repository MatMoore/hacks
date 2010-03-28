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

	def interValues(self, newVal, oldVal)
		return (newVal + (newVal-oldVal)*self.timeSinceUpdate)
		
	def interVector(self, newVec, oldVec)
		return newVec + (newVec-oldVec)*self.timeSinceUpdate

	@property
	def position
		return self.interVector(self._position, self._positionOld)
		
	@property
	def orientation
		return self.interVector(self._orientation, self._orientationOld)
