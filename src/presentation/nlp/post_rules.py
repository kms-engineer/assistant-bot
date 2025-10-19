import re
from typing import Dict

from .validators import (
    PhoneValidator,
    EmailValidator,
    DateValidator,
    AddressValidator,
    NameValidator,
    TagValidator,
    NoteValidator,
    IntentValidator
)


class PostProcessingRules:

    def __init__(self, default_region: str = "US"):
        self.default_region = default_region
        self._original_text = None  # Store original text for context-aware extraction

        # Initialize validators
        self.phone_validator = PhoneValidator(default_region=default_region)
        self.email_validator = EmailValidator()
        self.date_validator = DateValidator()
        self.address_validator = AddressValidator()
        self.name_validator = NameValidator()
        self.tag_validator = TagValidator()
        self.note_validator = NoteValidator()
        self.intent_validator = IntentValidator()

    def process(self, entities: Dict[str, str], intent: str) -> Dict[str, any]:
        processed = entities.copy()

        # Apply validators in sequence
        processed = self.phone_validator.validate(processed)
        processed = self.email_validator.validate(processed)
        processed = self.date_validator.validate(processed)
        processed = self.address_validator.validate(processed)
        processed = self.tag_validator.validate(processed)
        processed = self.name_validator.validate(processed)
        processed = self.note_validator.validate(processed)

        return processed

    def validate_entities_for_intent(self, entities: Dict, intent: str) -> Dict:
        return self.intent_validator.validate_for_intent(entities, intent)
