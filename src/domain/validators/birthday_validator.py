import re
from datetime import datetime
from typing import Dict, Optional

class BirthdayValidator:

    _pattern = re.compile(r"\d{2}\.\d{2}\.\d{4}")

    @staticmethod
    def validate(birthday: str, date_format: str = "%d.%m.%Y") -> bool | str:
        if not isinstance(birthday, str):
            return "Birthday must be a string"
        if not birthday or len(birthday.strip()) == 0:
            return "Birthday cannot be empty or whitespace"
        if not BirthdayValidator._pattern.fullmatch(birthday):
            return "Birthday contain invalid date format. Use DD.MM.YYYY"

        try:
            birthday_date = datetime.strptime(birthday, "%d.%m.%Y")
            today = datetime.now()

            if birthday_date > today:
                return "Birthday cannot be in future"
            if birthday_date.year < 1900:
                return f"Birthday contain invalid year: {birthday_date.year} (must be from 1900 onwards)"
            if not (1 <= birthday_date.month <= 12):
                return f"Birthday contain invalid month: {birthday_date:02d}"
            return True
        except ValueError:
            return f"Birthday contain invalid date: {birthday}"

    @staticmethod
    def validate_and_raise(birthday: str) -> None:
        result = BirthdayValidator.validate(birthday)
        if result is not True:
            raise ValueError(result)

    @staticmethod
    def normalize_for_nlp(entities: Dict) -> Dict:
        if 'birthday' not in entities or not entities['birthday']:
            return entities

        birthday_raw = entities['birthday']

        try:
            from dateutil import parser as date_parser

            # Parse date flexibly
            parsed_date = date_parser.parse(birthday_raw, fuzzy=True)

            # Normalize to DD.MM.YYYY (format expected by commands)
            entities['birthday'] = parsed_date.strftime('%d.%m.%Y')

            # Calculate age
            age = BirthdayValidator._calculate_age(parsed_date)
            entities['age'] = age

            # Add metadata
            entities['_birthday_valid'] = True

        except (ValueError, OverflowError, ImportError) as e:
            # Try manual parsing for common formats
            normalized = BirthdayValidator._manual_date_parse(birthday_raw)
            if normalized:
                entities['birthday'] = normalized
                # Try to calculate age (normalized is in DD.MM.YYYY format)
                try:
                    date_obj = datetime.strptime(normalized, '%d.%m.%Y')
                    age = BirthdayValidator._calculate_age(date_obj)
                    entities['age'] = age
                    entities['_birthday_valid'] = True
                except:
                    entities['_birthday_valid'] = False
            else:
                entities['_birthday_valid'] = False
                if '_validation_errors' not in entities:
                    entities['_validation_errors'] = []
                entities['_validation_errors'].append(f"Failed to parse birthday: {e}")

        return entities

    @staticmethod
    def _calculate_age(birth_date: datetime) -> int:
        today = datetime.today()
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
        return age

    @staticmethod
    def _manual_date_parse(date_str: str) -> Optional[str]:

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
