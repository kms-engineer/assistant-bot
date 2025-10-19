import re
from datetime import datetime
from typing import Dict, Optional
from dateutil import parser as date_parser

from .base import EntityValidator


class DateValidator(EntityValidator):

    def validate(self, entities: Dict) -> Dict:
        if 'birthday' not in entities or not entities['birthday']:
            return entities

        birthday_raw = entities['birthday']

        try:
            # Parse date flexibly
            parsed_date = date_parser.parse(birthday_raw, fuzzy=True)

            # Normalize to DD.MM.YYYY (format expected by commands)
            entities['birthday'] = parsed_date.strftime('%d.%m.%Y')

            # Calculate age
            age = self._calculate_age(parsed_date)
            entities['age'] = age

            # Add metadata
            entities['_birthday_valid'] = True

        except (ValueError, OverflowError) as e:
            # Try manual parsing for common formats
            normalized = self._manual_date_parse(birthday_raw)
            if normalized:
                entities['birthday'] = normalized
                # Try to calculate age (normalized is in DD.MM.YYYY format)
                try:
                    date_obj = datetime.strptime(normalized, '%d.%m.%Y')
                    age = self._calculate_age(date_obj)
                    entities['age'] = age
                    entities['_birthday_valid'] = True
                except:
                    entities['_birthday_valid'] = False
            else:
                entities['_birthday_valid'] = False
                self._add_error(entities, f"Failed to parse birthday: {e}")

        return entities

    def _calculate_age(self, birth_date: datetime) -> int:
        today = datetime.today()
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
        return age

    def _manual_date_parse(self, date_str: str) -> Optional[str]:
        """Parse date and return in DD.MM.YYYY format."""

        # DD.MM.YYYY or DD/MM/YYYY
        pattern1 = r'(\d{1,2})[./](\d{1,2})[./](\d{4})'
        match = re.match(pattern1, date_str)
        if match:
            day, month, year = match.groups()
            return f"{day.zfill(2)}.{month.zfill(2)}.{year}"

        # YYYY-MM-DD
        pattern2 = r'(\d{4})-(\d{1,2})-(\d{1,2})'
        match = re.match(pattern2, date_str)
        if match:
            year, month, day = match.groups()
            return f"{day.zfill(2)}.{month.zfill(2)}.{year}"

        # MM/DD/YYYY (US format)
        pattern3 = r'(\d{1,2})/(\d{1,2})/(\d{4})'
        match = re.match(pattern3, date_str)
        if match:
            month, day, year = match.groups()
            return f"{day.zfill(2)}.{month.zfill(2)}.{year}"

        return None
