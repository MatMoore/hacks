''' Deep math from wikipedia
These functions use angles in radians.'''

from constants import *
from math import *
from numpy import *

def rotationMatrix(axis, angle):
	'''Rotation matrix to rotate a vector about an axis'''
	c = cos(angle)
	s = sin(angle)
	ux,uy,uz = axis
	return array([\
			[(ux**2 + (1-ux**2) * c), (ux * uy * (1-c) - uz * s), (ux * uz * (1-c) + uy * s)], \
			[(ux * uy * (1-c) + uz * s), (uy**2 + (1-uy**2) * c), (uy*uz * (1-c) - ux * s)], \
			[(ux * uz * (1-c) - uy * s), (uy * uz * (1-c) + ux * s), (uz**2 + (1-uz**2) * c)]])

def angleBetween(vec1, vec2):
	'''The angle between two vectors'''
	d = dot(vec1,vec2)
	if d > 1: d = 1
	print d
	return acos(d/(linalg.norm(vec1)*linalg.norm(vec2)))

def integrate(x, v, a):
	return (x+v*TIMESTEP, v+a*TIMESTEP)

x = array([1,0,0])
y = array([0,1,0])
z = array([0,0,1])
