from pkg.constants.readonly import Readonly


class Role(Readonly):
	ADMIN = 'ADMIN'


class Regex(Readonly):
	USERNAME = r'^[a-zA-Z0-9._-]+$'
	PASSWORD = r'^[a-zA-Z0-9.@_-]+$'
