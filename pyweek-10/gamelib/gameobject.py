import constants
from numpy import *

class GameObject:
	def __init__(self):
		self._position = array([0.0, 0.0, 0.0])
		self._positionOld = array([0.0, 0.0, 0.0])

		# Which way "up" is pointing
		self._orientation = array([0.0, 0.0, 0.0])
		self._orientationOld = array([0.0, 0.0, 0.0])

		# Rotation about the self._orientation axis
		self._rotation = 0
		self._rotationOld = 0

		self.timeSinceUpdate = 0


	def update(self):
		self._orientationOld = self._orientation
		self._positionOld = self._position

	def interpolate(self, newVal, oldVal):
		return newVal + (newVal-oldVal)*self.timeSinceUpdate

	@property
	def position(self):
		return self.interpolate(self._position, self._positionOld)

	@property
	def orientation(self):
		return self.interpolate(self._orientation, self._orientationOld)

	@property
	def rotation(self)
		return self.interpolate(self._rotation, self._rotationOld)
