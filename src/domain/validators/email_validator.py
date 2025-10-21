import re
from typing import Union, Dict
from .string_validator import StringValidator


class EmailValidator:

    # Pre-compiled regex pattern for email validation
    # Basic email pattern: localpart@domain.tld
    _EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )

    # Error message constants
    ERROR_EMPTY = "Email cannot be empty or whitespace"
    ERROR_INVALID_FORMAT = "Email must be a valid email address (e.g., user@example.com)"

    @staticmethod
    def validate(email: str) -> Union[str, bool]:
        # Check if not empty
        if not StringValidator.is_not_empty(email):
            return EmailValidator.ERROR_EMPTY

        # Trim and convert to lowercase for validation
        trimmed_email = email.strip().lower()

        # Format validation: must match email pattern
        if not EmailValidator._EMAIL_PATTERN.fullmatch(trimmed_email):
            return EmailValidator.ERROR_INVALID_FORMAT

        return True

    @staticmethod
    def validate_and_raise(email: str) -> None:
        result = EmailValidator.validate(email)
        if result is not True:
            raise ValueError(result)

    @staticmethod
    def normalize_for_nlp(entities: Dict) -> Dict:
        if 'email' not in entities or not entities['email']:
            return entities

        email_raw = entities['email']

        try:
            from email_validator import validate_email, EmailNotValidError

            # Validate email
            validated = validate_email(email_raw, check_deliverability=False)
            entities['email'] = validated.normalized
            entities['_email_valid'] = True

        except EmailNotValidError as e:
            entities['_email_valid'] = False
            if '_validation_errors' not in entities:
                entities['_validation_errors'] = []
            entities['_validation_errors'].append(f"Invalid email: {e}")
        except ImportError:
            # Fallback to basic validation if library not available
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
