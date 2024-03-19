from os import getenv


class EnvVariableError(Exception):
	pass


def get_from_env(name: str) -> str:
	variable = getenv(name)

	if variable is None:
		raise EnvVariableError(f'Env variable {name} not found.')

	return variable