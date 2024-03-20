from marshmallow import validate


class Length(validate.Length):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.error = 'INVALID_LENGTH'


class Range(validate.Range):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.error = 'INVALID_RANGE'


class Regexp(validate.Regexp):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.error = 'REGEXP_MISMATCH'