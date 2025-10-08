import re


class PhoneValidator:

    @staticmethod
    def validate(phone: str) -> bool:
        if phone.startswith('+'):
            return bool(re.fullmatch(r"\+\d{11,15}", phone))
        return bool(re.fullmatch(r'\d{10}', phone))

    @staticmethod
    def normalize(raw: str) -> str:
        if raw.startswith('+'):
            normalized = '+' + re.sub(r"\D+", '', raw[1:])
        else:
            normalized = re.sub(r"\D+", '', raw)
        return normalized