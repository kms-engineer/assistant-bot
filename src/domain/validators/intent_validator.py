from typing import Dict
from src.config import IntentConfig


class IntentValidator:

    # Get required/optional entities from config
    # Extract from INTENT_REQUIREMENTS
    REQUIRED_ENTITIES = {
        intent: data['required']
        for intent, data in IntentConfig.INTENT_REQUIREMENTS.items()
    }

    OPTIONAL_ENTITIES = {
        intent: data['optional']
        for intent, data in IntentConfig.INTENT_REQUIREMENTS.items()
        if data['optional']  # Only include if there are optional entities
    }

    @staticmethod
    def validate_for_intent(entities: Dict, intent: str) -> Dict:
        required = IntentValidator.REQUIRED_ENTITIES.get(intent, [])
        optional = IntentValidator.OPTIONAL_ENTITIES.get(intent, [])
        missing = [field for field in required if field not in entities or not entities[field]]

        # Count how many optional entities are present
        optional_present = [field for field in optional if field in entities and entities[field]]

        # Check for format errors (e.g., invalid phone number format)
        has_format_errors = entities.get('_phone_format_error', False)

        # Validation is invalid if there are missing fields OR format errors
        is_valid = len(missing) == 0 and not has_format_errors

        return {
            'valid': is_valid,
            'missing': missing,
            'required': required,
            'optional': optional,
            'optional_present': optional_present,
            'has_optional': len(optional_present) > 0
        }
