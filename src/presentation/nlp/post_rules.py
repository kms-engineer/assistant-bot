import re
from typing import Dict, Any

# Import normalizers
from .normalizers import (
    PhoneNormalizer,
    EmailNormalizer,
    NameNormalizer,
    BirthdayNormalizer,
    AddressNormalizer,
    TagNormalizer,
    NoteTextNormalizer,
)

# Import validators (only for validation)
from ...domain.validators.intent_validator import IntentValidator
from ...config import NLPConfig, RegexPatterns


class PostProcessingRules:

    def __init__(self, default_region: str | None = None):
        self.default_region = default_region or NLPConfig.DEFAULT_REGION
        self._original_text = None  # Store original text for context-aware extraction

    def process(
        self, entities: Dict[str, str], intent: str, original_text: str | None = None
    ) -> Dict[str, Any]:
        processed: Dict[str, Any] = entities.copy()

        # Store original text for context-aware extraction
        if original_text:
            self._original_text = original_text

        # Special handling for edit_phone: extract old_phone and new_phone
        if intent == "edit_phone" and "phone" in processed:
            phone_value = str(processed["phone"])
            # Check if phone field contains both numbers (e.g., "123 to 456" or "123 456")
            # Try to extract two phone numbers from the original text if available
            if self._original_text:
                # Pattern: "from <old> to <new>" or "<old> to <new>"
                match = re.search(
                    RegexPatterns.POST_PHONE_FROM_TO_PATTERN,
                    self._original_text,
                    re.IGNORECASE,
                )
                if match:
                    old_phone_raw = re.sub(r"\D", "", match.group(1))
                    new_phone_raw = re.sub(r"\D", "", match.group(2))
                    processed["old_phone"] = old_phone_raw
                    processed["new_phone"] = new_phone_raw
                    # Remove the combined 'phone' field
                    if "phone" in processed:
                        del processed["phone"]
                else:
                    # Fallback: try to extract all phone numbers and take first two
                    all_phones = re.findall(
                        RegexPatterns.POST_PHONE_ALL_PATTERN, self._original_text
                    )
                    if len(all_phones) >= 2:
                        processed["old_phone"] = all_phones[0]
                        processed["new_phone"] = all_phones[1]
                        if "phone" in processed:
                            del processed["phone"]

        # Special handling for birthdays intents: normalize 'days' field
        if intent == "list_birthdays":
            # If 'days' field exists, extract only the number
            if "days" in processed:
                days_val = str(processed["days"])
                match = re.search(RegexPatterns.POST_DAYS_NUMBER_PATTERN, days_val)
                if match:
                    processed["days"] = int(match.group(1))

            # Remove 'address' field if it looks like days (contains only number and 'days')
            if "address" in processed:
                address_val = str(processed["address"]).lower()
                if re.match(RegexPatterns.POST_DAYS_IN_ADDRESS_PATTERN, address_val):
                    del processed["address"]

        # Apply normalizers
        # For edit_phone, normalize old_phone and new_phone separately
        if intent == "edit_phone":
            if "old_phone" in processed:
                old_phone_entities = {"phone": processed["old_phone"]}
                old_phone_entities = PhoneNormalizer.normalize(
                    old_phone_entities, self.default_region
                )
                processed["old_phone"] = old_phone_entities.get(
                    "phone", processed["old_phone"]
                )
                if "_phone_valid" in old_phone_entities:
                    processed["_old_phone_valid"] = old_phone_entities["_phone_valid"]
                if "_validation_errors" in old_phone_entities:
                    if "_validation_errors" not in processed:
                        processed["_validation_errors"] = []
                    processed["_validation_errors"].extend(
                        old_phone_entities["_validation_errors"]
                    )

            if "new_phone" in processed:
                new_phone_entities = {"phone": processed["new_phone"]}
                new_phone_entities = PhoneNormalizer.normalize(
                    new_phone_entities, self.default_region
                )
                processed["new_phone"] = new_phone_entities.get(
                    "phone", processed["new_phone"]
                )
                if "_phone_valid" in new_phone_entities:
                    processed["_new_phone_valid"] = new_phone_entities["_phone_valid"]
                if "_validation_errors" in new_phone_entities:
                    if "_validation_errors" not in processed:
                        processed["_validation_errors"] = []
                    processed["_validation_errors"].extend(
                        new_phone_entities["_validation_errors"]
                    )
        else:
            # Normal phone normalization for other intents
            processed = PhoneNormalizer.normalize(processed, self.default_region)

        processed = EmailNormalizer.normalize(processed)
        processed = BirthdayNormalizer.normalize(processed)
        processed = AddressNormalizer.normalize(processed)
        processed = TagNormalizer.normalize(processed)
        processed = NameNormalizer.normalize(processed)
        processed = NoteTextNormalizer.normalize(processed)

        return processed

    @staticmethod
    def validate_entities_for_intent(entities: Dict, intent: str) -> Dict:
        return IntentValidator.validate_for_intent(entities, intent)
