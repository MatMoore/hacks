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
	#print 'anglebetween'
	#print vec1
	#print vec2
	d = dot(vec1,vec2)
	if d > 1: d = 1
	elif d<-1: d = -1
	ab = linalg.norm(vec1) * linalg.norm(vec2)
	if ab == 0:
		print 'fuck'
		return 0
	# WTF why does this return math domain errors
	bla = d/ab
	try:
		bla2 = acos(bla)
	except:
		print 'd=%s' %d
		print 'ab=%s'% ab
		print str(bla)
		print acos.__doc__
		bla2 = 0
	return bla2

def integrate(x, v, a):
	return (x+v*TIMESTEP, v+a*TIMESTEP)

x = array([1,0,0])
y = array([0,1,0])
z = array([0,0,1])
