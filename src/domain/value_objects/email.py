import re
from .field import Field


class Email(Field):

    def __init__(self, value: str):
        if not self.validate(value):
            raise ValueError(f"Invalid email format: '{value}'")
        super().__init__(value)

    @staticmethod
    def validate(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
