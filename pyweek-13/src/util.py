from logging import debug
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

debug1 = run_once(debug)
