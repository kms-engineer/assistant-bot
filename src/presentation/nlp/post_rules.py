import re
from typing import Dict

# Import validators from domain layer
from ...domain.validators.phone_validator import PhoneValidator
from ...domain.validators.email_validator import EmailValidator
from ...domain.validators.birthday_validator import BirthdayValidator
from ...domain.validators.address_validator import AddressValidator
from ...domain.validators.name_validator import NameValidator
from ...domain.validators.tag_validator import TagValidator
from ...domain.validators.note_text_validator import NoteTextValidator
from ...domain.validators.intent_validator import IntentValidator
from ...config import NLPConfig


class PostProcessingRules:

    def __init__(self, default_region: str = None):
        self.default_region = default_region or NLPConfig.DEFAULT_REGION
        self._original_text = None  # Store original text for context-aware extraction

    def process(self, entities: Dict[str, str], intent: str) -> Dict[str, any]:
        processed = entities.copy()

        # Special handling for birthdays intents: normalize 'days' field
        if intent == 'list_birthdays':
            # If 'days' field exists, extract only the number
            if 'days' in processed:
                days_val = str(processed['days'])
                match = re.search(r'(\d+)', days_val)
                if match:
                    processed['days'] = int(match.group(1))

            # Remove 'address' field if it looks like days (contains only number and 'days')
            if 'address' in processed:
                address_val = str(processed['address']).lower()
                if re.match(r'^\d+\s*days?$', address_val):
                    del processed['address']

        # Apply normalizers using domain validators
        processed = PhoneValidator.normalize_for_nlp(processed, self.default_region)
        processed = EmailValidator.normalize_for_nlp(processed)
        processed = BirthdayValidator.normalize_for_nlp(processed)
        processed = AddressValidator.normalize_for_nlp(processed)
        processed = TagValidator.normalize_for_nlp(processed)
        processed = NameValidator.normalize_for_nlp(processed)
        processed = NoteTextValidator.normalize_for_nlp(processed)

        return processed

    def validate_entities_for_intent(self, entities: Dict, intent: str) -> Dict:
        return IntentValidator.validate_for_intent(entities, intent)
