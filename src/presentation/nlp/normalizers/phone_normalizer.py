from typing import Dict
from src.config import NLPConfig

try:
    import phonenumbers

    PHONENUMBERS_AVAILABLE = True
except ImportError:
    phonenumbers = None
    PHONENUMBERS_AVAILABLE = False


class PhoneNormalizer:

    @staticmethod
    def normalize(entities: Dict, default_region: str = None) -> Dict:
        if default_region is None:
            default_region = NLPConfig.DEFAULT_REGION

        if "phone" not in entities or not entities["phone"]:
            return entities

        phone_raw = entities["phone"]

        if not PHONENUMBERS_AVAILABLE:
            entities["_phone_valid"] = False
            if "_validation_errors" not in entities:
                entities["_validation_errors"] = []
            entities["_validation_errors"].append("phonenumbers library not available")
            return entities

        try:
            parsed_phone = phonenumbers.parse(phone_raw, default_region)

            if phonenumbers.is_valid_number(parsed_phone):
                entities["phone"] = phonenumbers.format_number(
                    parsed_phone, phonenumbers.PhoneNumberFormat.E164
                )
                entities["phone_national"] = phonenumbers.format_number(
                    parsed_phone, phonenumbers.PhoneNumberFormat.NATIONAL
                )
                entities["_phone_valid"] = True
            else:
                entities["_phone_valid"] = False
                if "_validation_errors" not in entities:
                    entities["_validation_errors"] = []
                entities["_validation_errors"].append(
                    f"Invalid phone number: {phone_raw}"
                )

        except Exception as e:
            entities["_phone_valid"] = False
            if "_validation_errors" not in entities:
                entities["_validation_errors"] = []
            entities["_validation_errors"].append(f"Failed to parse phone: {e}")

        return entities
