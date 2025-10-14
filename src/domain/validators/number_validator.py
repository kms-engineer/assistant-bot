class NumberValidator:
    @staticmethod
    def is_positive(number: int) -> bool:
        return number > 0

    @staticmethod
    def is_negative(number: int) -> bool:
        return number < 0

    @staticmethod
    def is_zero(number: int) -> bool:
        return number == 0

    @staticmethod
    def is_between(number: int, minimum: int, maximum: int) -> bool:
        return minimum <= number <= maximum
    
    @staticmethod
    def is_number(value: str) -> bool:
        if not value:
            return False
        return value.isdigit()