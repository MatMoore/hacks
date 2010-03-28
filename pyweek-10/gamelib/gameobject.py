import constants

class GameObject
	def __init__(physicsTimeStep):
		self._position = (0, 0, 0)
		self._positionOld = (0, 0, 0)
		self._orientation = (0, 0, 0)	#these might be really bad defaults
		self._orientationOld = (0, 0, 0)
		self.timeSinceUpdate = 0


	def update():
		pass

	def interValues(self, newVal, oldVal)
		return (newVal + (newVal-oldVal)*self.timeSinceUpdate)
		
	def interVector(self, newVec, oldVec)
		return (self.interValues(newVec[0], oldVec[0]), self.interValues(newVec[1], oldVec[1]), , self.interValues(newVec[2], oldVec[2]))

	@property
	def position
		return self.interVector(self._position, self._positionOld)
		
	@property
	def orientation
		return self.interVector(self._orientation, self._orientationOld)
