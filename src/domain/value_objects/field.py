from dataclasses import dataclass


@dataclass
class Field:
    value: any

    def __init__(self, value: any):
        self.value = value

    def __str__(self) -> str:
        return str(self.value) if self.value is not None else ""

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other) -> bool:
        return isinstance(other, Field) and self.value == other.value
