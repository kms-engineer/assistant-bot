import re
from typing import Union, Dict
from src.config import ValidationConfig, RegexPatterns, EntityConfig


class AddressValidator:

    MIN_LENGTH = ValidationConfig.ADDRESS_MIN_LENGTH
    MAX_LENGTH = ValidationConfig.ADDRESS_MAX_LENGTH

    # Pre-compiled regex pattern from config
    _ADDRESS_PATTERN = re.compile(RegexPatterns.VALIDATION_ADDRESS_PATTERN)
    _CITY_PATTERN = re.compile(RegexPatterns.ADDRESS_CITY_PATTERN)

    # Error message constants
    ERROR_EMPTY = "Address cannot be empty or whitespace"
    ERROR_TOO_SHORT = f"Address must be at least {MIN_LENGTH} characters long"
    ERROR_TOO_LONG = f"Address must be at most {MAX_LENGTH} characters long"
    ERROR_INVALID_CHARS = "Address contains invalid characters. Only letters, numbers, spaces, and basic punctuation (.,/-#) are allowed"

    @staticmethod
    def validate(address: str) -> Union[str, bool]:
        # Check if address is a string and not empty
        if not isinstance(address, str) or not address or len(address.strip()) == 0:
            return AddressValidator.ERROR_EMPTY

        # Trim for length validation
        trimmed_address = address.strip()

        # Check minimum length
        if len(trimmed_address) < AddressValidator.MIN_LENGTH:
            return AddressValidator.ERROR_TOO_SHORT

        # Check maximum length
        if len(trimmed_address) > AddressValidator.MAX_LENGTH:
            return AddressValidator.ERROR_TOO_LONG

        # Combined format validation: checks both allowed characters and alphanumeric requirement
        # Pattern uses positive lookahead (?=.*[a-zA-Z0-9]) to ensure at least one alphanumeric
        if not AddressValidator._ADDRESS_PATTERN.fullmatch(trimmed_address):
            return AddressValidator.ERROR_INVALID_CHARS

        return True

    @staticmethod
    def validate_and_raise(address: str) -> None:
        result = AddressValidator.validate(address)
        if result is not True:
            raise ValueError(result)

    @staticmethod
    def normalize_for_nlp(entities: Dict) -> Dict:
        if 'address' not in entities or not entities['address']:
            return entities

        address_raw = entities['address'].strip()

        # Try to extract city using pattern from config
        city_match = AddressValidator._CITY_PATTERN.search(address_raw)
        if city_match:
            entities['city'] = city_match.group(1)
        else:
            city_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b$'
            match = re.search(city_pattern, address_raw)
            if match:
                potential_city = match.group(1)
                # Exclude common street suffixes from config
                if potential_city.lower() not in EntityConfig.STREET_SUFFIXES_LOWER:
                    entities['city'] = potential_city

        # Normalize whitespace
        entities['address'] = re.sub(r'\s+', ' ', address_raw)

        return entities
