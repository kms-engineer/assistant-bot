import re


class PhoneValidator:

    @staticmethod
    def validate(phone: str) -> bool:
        return phone.isdigit() and len(phone) == 10

    @staticmethod
    def normalize(raw: str) -> str:
        return re.sub(r"\D+", "", raw)
