import random
import string


def random_user() -> str:
    """Return a random username 6 to 12 characters long containing only letters."""
    length = random.randint(12, 20)
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def random_phone() -> str:
    """Return a random phone number in the format +1-XXX-XXX-XXXX."""
    area_code = "".join(random.choice(string.digits) for _ in range(3))
    central_office_code = "".join(random.choice(string.digits) for _ in range(3))
    line_number = "".join(random.choice(string.digits) for _ in range(4))
    return f"+1-{area_code}-{central_office_code}-{line_number}"
