from typing import NamedTuple


class ApiError(Exception):
    status_code = 400


    def __init__(self, error_name, status_code=None, description=None):
        super().__init__

        self.error = error
        self.description = description

        if status_code is not None:
            self.status_code = status_code


    def to_dict(self):
        for_json = dict()
        for_json['message'] = self.error
        for_json['description'] = self.description

        return for_json


class ApiErrorInfo(NamedTuple):
    error_name: str
    status_code: Optional[int]
    description: Optional[str]