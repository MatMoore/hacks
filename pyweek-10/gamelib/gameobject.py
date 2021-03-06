from constants import *
from numpy import *

class GameObject(object):
	timeSinceUpdate = 0.0
	def __init__(self, position=None, orientation=None, facing=0):
		'''Orientation is a vector which points in the direction of "up" for this object. Facing is the angle the object is rotated about that axis.'''
		# Some defaults
		if position is None:
			position = array([0.0, 0.0, 0.0])
		if orientation is None:
			orientation = array([0.0, 0.0, 0.0])

		self._position = position.copy()
		self._positionOld = position.copy()

		# Which way "up" is pointing
		self._orientation = orientation.copy()
		self._orientationOld = orientation.copy()

		# Rotation about the self._orientation axis
		self._rotation = facing
		self._rotationOld = facing

		self.timeSinceUpdate = 0

	def update(self):
		self._orientationOld = self._orientation.copy()
		self._rotationOld = self._rotation
		self._positionOld = self._position.copy()

	def interpolate(self, newVal, oldVal):
		return newVal + (newVal-oldVal)*GameObject.timeSinceUpdate

	@property
	def position(self):
		return self.interpolate(self._position, self._positionOld)

	@property
	def orientation(self):
		return self.interpolate(self._orientation, self._orientationOld)

	@property
	def rotation(self):
		return self.interpolate(self._rotation, self._rotationOld)
