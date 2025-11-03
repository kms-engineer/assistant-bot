from abc import ABC, abstractmethod
from typing import Union


class BaseValidator(ABC):

    @staticmethod
    @abstractmethod
    def validate(value: str) -> Union[str, bool]:
        pass

    @classmethod
    def validate_and_raise(cls, value: str) -> None:
        result = cls.validate(value)
        if result is not True:
            raise ValueError(result)

    @staticmethod
    def is_empty_string(string):
        return not isinstance(string, str) or not string or len(string.strip()) == 0
