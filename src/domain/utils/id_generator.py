import uuid
from typing import Set, Callable


class IDGenerator:

    @staticmethod
    def generate_unique_id(existing_ids_provider: Callable[[], Set[str]]) -> str:
        max_attempts = 100
        for _ in range(max_attempts):
            new_id = str(uuid.uuid4())
            if new_id not in existing_ids_provider():
                return new_id

        raise RuntimeError("Unable to generate unique ID after maximum attempts")

    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())
