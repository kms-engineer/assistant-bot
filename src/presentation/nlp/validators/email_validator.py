from typing import Dict
from email_validator import validate_email, EmailNotValidError

from .base import EntityValidator


class EmailValidator(EntityValidator):

    def validate(self, entities: Dict) -> Dict:
        if 'email' not in entities or not entities['email']:
            return entities

        email_raw = entities['email']

        try:
            # Validate email
            validated = validate_email(email_raw, check_deliverability=False)
            entities['email'] = validated.normalized
            entities['_email_valid'] = True

        except EmailNotValidError as e:
            entities['_email_valid'] = False
            self._add_error(entities, f"Invalid email: {e}")

        return entities
