class Constant:
	def __setattr__():
		raise AttributeError('Cannot set constant attribute')

	def __delattr__():
		raise AttributeError('Cannot delete constant attribute')