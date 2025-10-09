import re
from typing import Optional, Tuple, List

QUOTED_GROUP = r'"([^"]+)"'
TOKEN_GROUP = r'(\S+)'
ANY_LAZY_GROUP = r'(.+?)'


def pick_first(*values: Optional[str]) -> str:
    for value in values:
        if value is not None:
            return value
    return ""


def trimmed(text: Optional[str]) -> str:
    return text.strip() if text else ""


class RegexCommandGate:
    @staticmethod
    def match(raw_input: str) -> Optional[Tuple[str, List[str]]]:
        if not raw_input or not raw_input.strip():
            return None
        line = raw_input.strip()

        hello_match = re.fullmatch(r'hello', line, flags=re.IGNORECASE)
        if hello_match:
            return "hello", []

        add_match = re.fullmatch(rf'add\s+{TOKEN_GROUP}\s+{TOKEN_GROUP}', line, flags=re.IGNORECASE)
        if add_match:
            return "add", [add_match.group(1), add_match.group(2)]

        change_match = re.fullmatch(rf'change\s+{TOKEN_GROUP}\s+{TOKEN_GROUP}\s+{TOKEN_GROUP}', line, flags=re.IGNORECASE)
        if change_match:
            return "change", [change_match.group(1), change_match.group(2), change_match.group(3)]

        delete_contact_match = re.fullmatch(rf'delete-contact\s+{TOKEN_GROUP}', line, flags=re.IGNORECASE)
        if delete_contact_match:
            return "delete-contact", [delete_contact_match.group(1)]

        phone_match = re.fullmatch(rf'phone\s+{TOKEN_GROUP}', line, flags=re.IGNORECASE)
        if phone_match:
            return "phone", [phone_match.group(1)]

        all_match = re.fullmatch(r'all', line, flags=re.IGNORECASE)
        if all_match:
            return "all", []

        add_birthday_match = re.fullmatch(rf'add-birthday\s+{TOKEN_GROUP}\s+{TOKEN_GROUP}', line, flags=re.IGNORECASE)
        if add_birthday_match:
            return "add-birthday", [add_birthday_match.group(1), add_birthday_match.group(2)]

        show_birthday_match = re.fullmatch(rf'show-birthday\s+{TOKEN_GROUP}', line, flags=re.IGNORECASE)
        if show_birthday_match:
            return "show-birthday", [show_birthday_match.group(1)]

        birthdays_match = re.fullmatch(r'birthdays', line, flags=re.IGNORECASE)
        if birthdays_match:
            return "birthdays", []

        add_email_match = re.fullmatch(rf'add-email\s+{TOKEN_GROUP}\s+{TOKEN_GROUP}', line, flags=re.IGNORECASE)
        if add_email_match:
            return "add-email", [add_email_match.group(1), add_email_match.group(2)]

        add_address_match = re.fullmatch(
            rf'add-address\s+{TOKEN_GROUP}\s+(?:{QUOTED_GROUP}|{ANY_LAZY_GROUP})',
            line,
            flags=re.IGNORECASE
        )
        if add_address_match:
            contact_name = add_address_match.group(1)
            address_value = pick_first(add_address_match.group(2), add_address_match.group(3))
            return "add-address", [contact_name, trimmed(address_value)]

        save_match = re.fullmatch(rf'save\s+(?:{QUOTED_GROUP}|{TOKEN_GROUP})', line, flags=re.IGNORECASE)
        if save_match:
            filename_value = pick_first(save_match.group(1), save_match.group(2))
            return "save", [filename_value]

        load_match = re.fullmatch(rf'load\s+(?:{QUOTED_GROUP}|{TOKEN_GROUP})', line, flags=re.IGNORECASE)
        if load_match:
            filename_value = pick_first(load_match.group(1), load_match.group(2))
            return "load", [filename_value]

        exit_match = re.fullmatch(r'close|exit', line, flags=re.IGNORECASE)
        if exit_match:
            return "exit", []

        return None
