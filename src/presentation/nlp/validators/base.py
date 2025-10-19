from abc import ABC, abstractmethod
from typing import Dict, List


class ValidationResult:

    def __init__(self, valid: bool = True, errors: List[str] = None):
        self.valid = valid
        self.errors = errors or []

    def add_error(self, error: str):
        self.errors.append(error)
        self.valid = False


class EntityValidator(ABC):

    @abstractmethod
    def validate(self, entities: Dict) -> Dict:
        pass

    def _add_error(self, entities: Dict, error: str) -> Dict:
        if '_validation_errors' not in entities:
            entities['_validation_errors'] = []
        entities['_validation_errors'].append(error)
        return entities
