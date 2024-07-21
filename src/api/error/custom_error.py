from typing import NamedTuple, TypedDict, Optional


class ApiErrorInfo(NamedTuple):
    error_message: str
    field_name: Optional[str] = None
    status_code: Optional[int] = None
    description: Optional[str] = None


class ApiErrorForJson(TypedDict):
    message: str
    fieldName: Optional[str]
    description: Optional[str]


class ApiError(Exception):
    status_code = 400
    validation_errors = None


    def __init__(self, error_info: ApiErrorInfo | list[ApiErrorInfo]):
        super().__init__

        if isinstance(error_info, ApiErrorInfo):
            self.error = error_info.error_message
            self.description = error_info.description
            self.field_name = error_info.field_name

            if error_info.status_code is not None:
                self.status_code = error_info.status_code
        else:
            self.validation_errors = error_info


    def to_dict(self) -> ApiErrorForJson | list[ApiErrorForJson]:
        if not validation_errors:
            for_json = ApiErrorForJson(
                message = self.error,
                fieldName = self.field_name,
                description = self.description
            )
            return for_json

        for_json = []
        for validation_error in validation_errors:
            error = ApiErrorForJson(
                message = validation_error.message,
                fieldName = validation_error.field_name
            )
            for_json.append(error)

        return for_json
