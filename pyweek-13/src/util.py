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

class Timer(object):
	def __init__(self, period_ms):
		self.period = period_ms
		self.t = 0
		object.__init__(self)

	def check(self, ms):
		self.t += ms
		if self.t >= self.period:
			self.t = 0
			return True
		return False

debug1 = run_once(debug)
