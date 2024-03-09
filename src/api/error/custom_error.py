from typing import NamedTuple, TypedDict, Optional


class ApiErrorInfo(NamedTuple):
    error_message: str | dict
    status_code: Optional[int] = None
    description: Optional[str] = None


class ApiErrorForJson(TypedDict):
    message: str
    description: Optional[str]


class ApiError(Exception):
    status_code = 400


    def __init__(self, error_info: ApiErrorInfo):
        super().__init__

        self.error = error_info.error_message
        self.description = error_info.description

        if error_info.status_code is not None:
            self.status_code = error_info.status_code


    def to_dict(self) -> ApiErrorForJson:
        for_json = ApiErrorForJson()
        for_json['message'] = self.error
        for_json['description'] = self.description

        return for_json