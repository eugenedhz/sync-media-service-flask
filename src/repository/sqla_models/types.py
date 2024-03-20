from sqlalchemy.types import TypeDecorator
from sqlalchemy import DateTime
from datetime import datetime


class DateAsTimestamp(TypeDecorator):
    cache_ok = True
    impl = DateTime

    def process_bind_param(self, value, dialect):
        if value is not None:
            return datetime.fromtimestamp(value)

    def process_result_value(self, value, dialect):
        if value is not None:
            return int(value.timestamp())