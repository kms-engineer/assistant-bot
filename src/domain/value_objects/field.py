
class Field:

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other) -> bool:
        return isinstance(other, Field) and self.value == other.value
