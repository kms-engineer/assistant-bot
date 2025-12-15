from typing import Optional, List, Tuple

from src.domain.validators.phone_validator import PhoneValidator
from src.domain.validators.email_validator import EmailValidator
from src.domain.validators.birthday_validator import BirthdayValidator
from src.domain.validators.address_validator import AddressValidator
from src.domain.validators.name_validator import NameValidator
from src.presentation.cli.interactive_input import InteractiveInputBuilder, InputResult


def _validate_wrapper(validator_class):
    def validator(value: str) -> bool:
        result = validator_class.validate(value)
        return result is True
    return validator


def _get_error_message(validator_class, value: str) -> str:
    result = validator_class.validate(value)
    if result is True:
        return ""
    return result if isinstance(result, str) else "Invalid value"


class InteractiveAddContact:
    def collect(self) -> InputResult:
        builder = InteractiveInputBuilder()

        builder.add_field(
            name="name",
            prompt="Contact name",
            required=True,
            validator=_validate_wrapper(NameValidator),
            error_message="Name must be 2-50 characters, letters and spaces only",
        )

        builder.add_field(
            name="phone",
            prompt="Phone number",
            required=True,
            validator=_validate_wrapper(PhoneValidator),
            error_message="Phone must be 8-15 digits, can start with +",
        )

        builder.add_field(
            name="email",
            prompt="Email address",
            required=False,
            validator=_validate_wrapper(EmailValidator),
            error_message="Invalid email format",
        )

        builder.add_field(
            name="birthday",
            prompt="Birthday (DD.MM.YYYY)",
            required=False,
            validator=_validate_wrapper(BirthdayValidator),
            error_message="Invalid date format, use DD.MM.YYYY",
        )

        builder.add_field(
            name="address",
            prompt="Address",
            required=False,
            validator=_validate_wrapper(AddressValidator),
            error_message="Address must be 5-200 characters",
        )

        return builder.build()


class InteractiveAddNote:
    def collect(self) -> InputResult:
        builder = InteractiveInputBuilder()

        builder.add_field(
            name="title",
            prompt="Note title",
            required=True,
            validator=lambda x: len(x.strip()) > 0,
            error_message="Title cannot be empty",
        )

        builder.add_field(
            name="text",
            prompt="Note text",
            required=True,
            validator=lambda x: len(x.strip()) > 0,
            error_message="Text cannot be empty",
        )

        builder.add_field(
            name="tags",
            prompt="Tags (comma-separated)",
            required=False,
            transform=lambda x: [t.strip() for t in x.split(",") if t.strip()],
        )

        return builder.build()


class InteractiveChangePhone:
    def __init__(self, contact_names: Optional[List[str]] = None):
        self._contact_names = contact_names or []

    def collect(self) -> InputResult:
        builder = InteractiveInputBuilder()

        builder.add_field(
            name="name",
            prompt="Contact name",
            required=True,
            validator=_validate_wrapper(NameValidator),
            error_message="Invalid contact name",
            completer_options=self._contact_names,
        )

        builder.add_field(
            name="old_phone",
            prompt="Current phone number",
            required=True,
            validator=_validate_wrapper(PhoneValidator),
            error_message="Invalid phone format",
        )

        builder.add_field(
            name="new_phone",
            prompt="New phone number",
            required=True,
            validator=_validate_wrapper(PhoneValidator),
            error_message="Invalid phone format",
        )

        return builder.build()


class InteractiveAddEmail:
    def __init__(self, contact_names: Optional[List[str]] = None):
        self._contact_names = contact_names or []

    def collect(self) -> InputResult:
        builder = InteractiveInputBuilder()

        builder.add_field(
            name="name",
            prompt="Contact name",
            required=True,
            completer_options=self._contact_names,
        )

        builder.add_field(
            name="email",
            prompt="Email address",
            required=True,
            validator=_validate_wrapper(EmailValidator),
            error_message="Invalid email format",
        )

        return builder.build()


class InteractiveAddBirthday:
    def __init__(self, contact_names: Optional[List[str]] = None):
        self._contact_names = contact_names or []

    def collect(self) -> InputResult:
        builder = InteractiveInputBuilder()

        builder.add_field(
            name="name",
            prompt="Contact name",
            required=True,
            completer_options=self._contact_names,
        )

        builder.add_field(
            name="birthday",
            prompt="Birthday (DD.MM.YYYY)",
            required=True,
            validator=_validate_wrapper(BirthdayValidator),
            error_message="Invalid date format, use DD.MM.YYYY",
        )

        return builder.build()


class InteractiveAddAddress:
    def __init__(self, contact_names: Optional[List[str]] = None):
        self._contact_names = contact_names or []

    def collect(self) -> InputResult:
        builder = InteractiveInputBuilder()

        builder.add_field(
            name="name",
            prompt="Contact name",
            required=True,
            completer_options=self._contact_names,
        )

        builder.add_field(
            name="address",
            prompt="Address",
            required=True,
            validator=_validate_wrapper(AddressValidator),
            error_message="Address must be 5-200 characters",
        )

        return builder.build()


def interactive_add_contact() -> Optional[Tuple[str, List[str]]]:
    collector = InteractiveAddContact()
    result = collector.collect()

    if not result.success:
        return None

    args = [result.values["name"], result.values["phone"]]

    optional_args = {}
    if "email" in result.values and result.values["email"]:
        optional_args["email"] = result.values["email"]
    if "birthday" in result.values and result.values["birthday"]:
        optional_args["birthday"] = result.values["birthday"]
    if "address" in result.values and result.values["address"]:
        optional_args["address"] = result.values["address"]

    return args, optional_args


def interactive_add_note() -> Optional[Tuple[List[str], List[str]]]:
    collector = InteractiveAddNote()
    result = collector.collect()

    if not result.success:
        return None

    args = [result.values["title"], result.values["text"]]
    tags = result.values.get("tags", [])

    return args, tags


def interactive_change_phone(contact_names: List[str] = None) -> Optional[List[str]]:
    collector = InteractiveChangePhone(contact_names)
    result = collector.collect()

    if not result.success:
        return None

    return [
        result.values["name"],
        result.values["old_phone"],
        result.values["new_phone"],
    ]
