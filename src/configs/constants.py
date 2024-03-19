class Constant:
	def __setattr__():
		raise AttributeError('Cannot set constant attribute')

	def __delattr__():
		raise AttributeError('Cannot delete constant attribute')


class Role(Constant):
	ADMIN = 'ADMIN'


class Regex(Constant):
	USERNAME = r'^[a-zA-Z0-9._-]+$'
	PASSWORD = r'^[a-zA-Z0-9.@_-]+$'
