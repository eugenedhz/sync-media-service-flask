from pkg.constants.constant import Constant


class Role(Constant):
	ADMIN = 'ADMIN'


class Regex(Constant):
	USERNAME = r'^[a-zA-Z0-9._-]+$'
	PASSWORD = r'^[a-zA-Z0-9.@_-]+$'
