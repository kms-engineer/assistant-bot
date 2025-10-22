import re
from typing import Dict, Optional
from src.config import PhoneConfig, NLPConfig

class PhoneValidator:

    @staticmethod
    def validate(phone: str) -> str | bool:
        if not isinstance(phone, str):
            return "Phone number must be string value"
        if len(phone) != PhoneConfig.EXACT_PHONE_LENGTH:
            return f"Phone number must be exactly {PhoneConfig.EXACT_PHONE_LENGTH} digits long"
        if not phone.isdigit():
            return "Phone number must contain only digits"
        return True

    @staticmethod
    def validate_and_raise(phone: str) -> None:
        result = PhoneValidator.validate(phone)
        if result is not True:
            raise ValueError(result)

    @staticmethod
    def normalize(raw: str) -> str:
        if not raw: return ""
        if raw.startswith('+'):
            normalized = re.sub(r"\D+", '', raw[1:])
        else:
            normalized = re.sub(r"\D+", '', raw)
        return normalized

    @staticmethod
    def normalize_for_nlp(entities: Dict, default_region: str = None) -> Dict:
        if default_region is None:
            default_region = NLPConfig.DEFAULT_REGION
        if 'phone' not in entities or not entities['phone']:
            return entities

        phone_raw = entities['phone']

        try:
            import phonenumbers
            from phonenumbers import NumberParseException

            parsed_phone = phonenumbers.parse(phone_raw, default_region)

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
                if '_validation_errors' not in entities:
                    entities['_validation_errors'] = []
                entities['_validation_errors'].append(f"Invalid phone number: {phone_raw}")

        except (NumberParseException, ImportError) as e:
            # Keep original if parsing fails or library not available
            entities['_phone_valid'] = False
            if '_validation_errors' not in entities:
                entities['_validation_errors'] = []
            entities['_validation_errors'].append(f"Failed to parse phone: {e}")

        return entities