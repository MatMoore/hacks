from logging import debug
from itertools import cycle
import traceback

def memoize(f):
	cache = {}
	def new(*args):
		args = tuple(args)
		try:
			return cache[args]
		except KeyError:
			# Cache miss
			value = f(*args)
			cache[args] = value
			return value
		except TypeError:
			# Unhashable args
			return f(*args)
	return new

def run_once(f):
	'''Don't run the same thing twice'''
	run = set()
	def new(*args, **kwargs):
		stack = tuple(traceback.extract_stack())
		if stack not in run:
			f(*args, **kwargs)
			run.add(stack)
	return new

def throttle(n):
	'''Only allow 1 in every n function calls'''
	def wrap(f):
		allowed = cycle((i == 0 for i in xrange(n)))
		def new(*args, **kwargs):
			if allowed.next():
				f(*args, **kwargs)
		return new
	return wrap


debug1 = run_once(debug)
