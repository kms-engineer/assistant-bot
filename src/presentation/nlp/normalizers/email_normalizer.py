from typing import Dict
from src.domain.validators.email_validator import EmailValidator

try:
    from email_validator import validate_email
    EMAIL_VALIDATOR_AVAILABLE = True
except ImportError:
    validate_email = None
    EMAIL_VALIDATOR_AVAILABLE = False


class EmailNormalizer:

    @staticmethod
    def normalize(entities: Dict) -> Dict:
        if 'email' not in entities or not entities['email']:
            return entities

        email_raw = entities['email']

        if EMAIL_VALIDATOR_AVAILABLE:
            try:
                validated = validate_email(email_raw, check_deliverability=False)
                entities['email'] = validated.normalized
                entities['_email_valid'] = True
            except Exception as e:
                entities['_email_valid'] = False
                if '_validation_errors' not in entities:
                    entities['_validation_errors'] = []
                entities['_validation_errors'].append(f"Invalid email: {e}")
        else:
            result = EmailValidator.validate(email_raw)
            if result is True:
                entities['email'] = email_raw.strip().lower()
                entities['_email_valid'] = True
            else:
                entities['_email_valid'] = False
                if '_validation_errors' not in entities:
                    entities['_validation_errors'] = []
                entities['_validation_errors'].append(str(result))

        return entities
