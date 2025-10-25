import os
from difflib import get_close_matches
from typing import Dict, Callable, List

from .error_handler import handle_errors
from .ui_messages import UIMessages
from ...application.commands import contact_commands, note_commands
from ...application.services.contact_service import ContactService
from ...application.services.note_service import NoteService


class CommandHandler:

    def __init__(self, contact_service: ContactService, note_service: NoteService):
        self.contact_service = contact_service
        self.note_service = note_service
        self.commands: Dict[str, Callable] = {
            "hello": self._wrap(contact_commands.hello),
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
            "search": self._wrap(contact_commands.search),
            "find": self._wrap(contact_commands.find),
            # Note commands
            "add-note": self._wrap_note(note_commands.add_note),
            "show-notes": self._wrap_note(note_commands.show_notes),
            "edit-note": self._wrap_note(note_commands.edit_note),
            "delete-note": self._wrap_note(note_commands.delete_note),
            # Note tag commands
            "add-tag": self._wrap_note(note_commands.add_tag),
            "remove-tag": self._wrap_note(note_commands.remove_tag),
            "search-notes": self._wrap_note(note_commands.search_notes),
            "search-notes-by-tag": self._wrap_note(note_commands.search_notes_by_tag),
            "list-tags": self._wrap_note(note_commands.list_tags)
        }

    def _wrap(self, command_func: Callable) -> Callable:
        @handle_errors
        def wrapper(args: List[str]) -> str:
            return command_func(args, self.contact_service)

        return wrapper

    def _wrap_note(self, command_func: Callable) -> Callable:
        """Wrapper for note commands"""

        @handle_errors
        def wrapper(args: List[str]) -> str:
            return command_func(args, self.note_service)

        return wrapper

    def handle(self, command: str, args: List[str]) -> str:
        if command in ("close", "exit"):
            return "exit"

        if command == 'help':
            return UIMessages.COMMAND_LIST

        if command == 'clear':
            os.system('cls') if os.name == 'nt' else os.system('clear')
            return command

        if command in self.commands:
            return self.commands[command](args)

        available = [*self.commands.keys(), "close", "exit"]
        suggestion = get_close_matches(command, available, n=1, cutoff=0.6)
        return UIMessages.invalid_command(available, suggestion[0] if suggestion else None)
