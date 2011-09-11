class Director(object):
	def __init__(self):
		self.current = None

	@classmethod
	def mediate(form, handler_method, doc=None):
		'''Tell Director class to mediate some event. This adds a method to the director object which delegates to the handler_method of the currently active scene.'''
		def handler(self, *args, **kwargs):
			if self.current:
				self.current.handler_method(*args, **kwargs)
		handler.__doc__ = doc or "Calls the equivalent method on the currently active scene"
		form.handler_method = handler
