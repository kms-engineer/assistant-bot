from .field import Field


class Tag(Field):

    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("Tag cannot be empty")
        if len(value) > 50:
            raise ValueError("Tag too long (max 50 characters)")
        super().__init__(value.strip())
