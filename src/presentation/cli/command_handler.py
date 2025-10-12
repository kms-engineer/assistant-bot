from typing import Dict, Callable, List
from difflib import get_close_matches
from ...application.services.contact_service import ContactService
from ...application.commands import contact_commands
from .error_handler import handle_errors
from .ui_messages import UIMessages


class CommandHandler:

    def __init__(self, contact_service: ContactService):
        self.contact_service = contact_service
        self.commands: Dict[str, Callable] = {
            "hello": self._wrap(contact_commands.hello),
            "help": self._wrap(contact_commands.help),
            "add": self._wrap(contact_commands.add_contact),
            "change": self._wrap(contact_commands.change_contact),
            "delete-contact": self._wrap(contact_commands.delete_contact),
            "phone": self._wrap(contact_commands.show_phone),
            "all": self._wrap(contact_commands.show_all),
            "add-birthday": self._wrap(contact_commands.add_birthday),
            "show-birthday": self._wrap(contact_commands.show_birthday),
            "birthdays": self._wrap(contact_commands.birthdays),
            "add-email": self._wrap(contact_commands.add_email),
            "edit-email": self._wrap(contact_commands.edit_email),
            "remove-email": self._wrap(contact_commands.remove_email),
            "add-address": self._wrap(contact_commands.add_address),
            "edit-address": self._wrap(contact_commands.edit_address),
            "remove-address": self._wrap(contact_commands.remove_address),
            "save": self._wrap(contact_commands.save_contacts),
            "load": self._wrap(contact_commands.load_contacts),
        }

    def _wrap(self, command_func: Callable) -> Callable:
        @handle_errors
        def wrapper(args: List[str]) -> str:
            return command_func(args, self.contact_service)
        return wrapper

    def handle(self, command: str, args: List[str]) -> str:
        if command in ("close", "exit"):
            return "exit"

        if command in self.commands:
            return self.commands[command](args)

        available = [*self.commands.keys(), "close", "exit"]
        suggestion = get_close_matches(command, available, n=1, cutoff=0.6)
        return UIMessages.invalid_command(available, suggestion[0] if suggestion else None)
