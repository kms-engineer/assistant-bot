import re
from typing import Union, Dict
from .string_validator import StringValidator


class NameValidator:

    MIN_LENGTH = 2
    MAX_LENGTH = 50

    # Pre-compiled regex pattern for performance
    # Allows letters (any language), spaces, hyphens, and apostrophes
    _NAME_PATTERN = re.compile(r'^[a-zA-ZÀ-ÿ\s\-\']+$')

    # Error message constants
    ERROR_EMPTY = "Name cannot be empty or whitespace"
    ERROR_TOO_SHORT = f"Name must be at least {MIN_LENGTH} characters long"
    ERROR_TOO_LONG = f"Name must be at most {MAX_LENGTH} characters long"
    ERROR_INVALID_CHARS = "Name can only contain letters, spaces, and hyphens"

    @staticmethod
    def validate(name: str) -> Union[str, bool]:
        # Check if not empty
        if not StringValidator.is_not_empty(name):
            return NameValidator.ERROR_EMPTY

        # Trim for length validation
        trimmed_name = name.strip()

        # Check minimum length
        if not StringValidator.has_min_length(trimmed_name, NameValidator.MIN_LENGTH):
            return NameValidator.ERROR_TOO_SHORT

        # Check maximum length
        if not StringValidator.has_max_length(trimmed_name, NameValidator.MAX_LENGTH):
            return NameValidator.ERROR_TOO_LONG

        # Format validation: only letters, spaces, hyphens
        if not NameValidator._NAME_PATTERN.fullmatch(trimmed_name):
            return NameValidator.ERROR_INVALID_CHARS

        return True

    @staticmethod
    def validate_and_raise(name: str) -> None:
        result = NameValidator.validate(name)
        if result is not True:
            raise ValueError(result)

    @staticmethod
    def normalize_for_nlp(entities: Dict) -> Dict:
        if 'name' not in entities or not entities['name']:
            return entities

        name_raw = entities['name'].strip()

        # Capitalize each word
        name_cleaned = ' '.join(word.capitalize() for word in name_raw.split())

        # Remove extra whitespace
        name_cleaned = re.sub(r'\s+', ' ', name_cleaned)

        entities['name'] = name_cleaned

        # Validate: should have at least 2 characters
        if len(name_cleaned) < 2:
            entities['_name_valid'] = False
            if '_validation_errors' not in entities:
                entities['_validation_errors'] = []
            entities['_validation_errors'].append(f"Name too short: {name_cleaned}")
        else:
            entities['_name_valid'] = True

        return entities
