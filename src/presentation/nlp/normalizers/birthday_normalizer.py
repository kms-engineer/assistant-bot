import re
from datetime import datetime
from typing import Dict, Optional
from src.config import RegexPatterns

try:
    from dateutil import parser as date_parser

    DATEUTIL_AVAILABLE = True
except ImportError:
    date_parser = None
    DATEUTIL_AVAILABLE = False


class BirthdayNormalizer:

    @staticmethod
    def normalize(entities: Dict) -> Dict:
        if "birthday" not in entities or not entities["birthday"]:
            return entities

        birthday_raw = entities["birthday"]

        if DATEUTIL_AVAILABLE:
            try:
                parsed_date = date_parser.parse(birthday_raw, fuzzy=True)
                entities["birthday"] = parsed_date.strftime("%d.%m.%Y")
                entities["age"] = BirthdayNormalizer._calculate_age(parsed_date)
                entities["_birthday_valid"] = True
                return entities
            except (ValueError, OverflowError) as e:
                pass

        # Fallback to manual parsing
        normalized = BirthdayNormalizer._manual_date_parse(birthday_raw)
        if normalized:
            entities["birthday"] = normalized
            try:
                date_obj = datetime.strptime(normalized, "%d.%m.%Y")
                entities["age"] = BirthdayNormalizer._calculate_age(date_obj)
                entities["_birthday_valid"] = True
            except ValueError:
                entities["_birthday_valid"] = False
        else:
            entities["_birthday_valid"] = False
            if "_validation_errors" not in entities:
                entities["_validation_errors"] = []
            entities["_validation_errors"].append(
                f"Failed to parse birthday: {birthday_raw}"
            )

        return entities

    @staticmethod
    def _calculate_age(birth_date: datetime) -> int:
        today = datetime.today()
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
        return age

    @staticmethod
    def _manual_date_parse(date_str: str) -> Optional[str]:
        match = re.match(RegexPatterns.BIRTHDAY_PARSE_DD_MM_YYYY, date_str)
        if match:
            day, month, year = match.groups()
            return f"{day.zfill(2)}.{month.zfill(2)}.{year}"

        match = re.match(RegexPatterns.BIRTHDAY_PARSE_YYYY_MM_DD, date_str)
        if match:
            year, month, day = match.groups()
            return f"{day.zfill(2)}.{month.zfill(2)}.{year}"

        match = re.match(RegexPatterns.BIRTHDAY_PARSE_MM_DD_YYYY, date_str)
        if match:
            month, day, year = match.groups()
            return f"{day.zfill(2)}.{month.zfill(2)}.{year}"

        return None
