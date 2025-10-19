from typing import Dict
import phonenumbers
from phonenumbers import NumberParseException

from .base import EntityValidator


class PhoneValidator(EntityValidator):

    def __init__(self, default_region: str = "US"):
        self.default_region = default_region

    def validate(self, entities: Dict) -> Dict:
        if 'phone' not in entities or not entities['phone']:
            return entities

        phone_raw = entities['phone']

        try:
            parsed_phone = phonenumbers.parse(phone_raw, self.default_region)

            if phonenumbers.is_valid_number(parsed_phone):
                # E.164 format (international)
                entities['phone'] = phonenumbers.format_number(
                    parsed_phone,
                    phonenumbers.PhoneNumberFormat.E164
                )

                # National format (human-readable)
                entities['phone_national'] = phonenumbers.format_number(
                    parsed_phone,
                    phonenumbers.PhoneNumberFormat.NATIONAL
                )

                # Add metadata
                entities['_phone_valid'] = True
            else:
                entities['_phone_valid'] = False
                self._add_error(entities, f"Invalid phone number: {phone_raw}")

        except NumberParseException as e:
            # Keep original if parsing fails
            entities['_phone_valid'] = False
            self._add_error(entities, f"Failed to parse phone: {e}")

        return entities
