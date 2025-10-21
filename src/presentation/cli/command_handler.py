from typing import Dict, Callable, List
from difflib import get_close_matches
from ...application.services.contact_service import ContactService
from ...application.services.note_service import NoteService
from ...application.commands import contact_commands, note_commands
from .error_handler import handle_errors
from .ui_messages import UIMessages


class CommandHandler:

    def __init__(self, contact_service: ContactService, note_service: NoteService, nlp_mode: bool = False):
        self.contact_service = contact_service
        self.note_service = note_service
        self.nlp_mode = nlp_mode
        self.commands: Dict[str, Callable] = {
            "hello": self._wrap(contact_commands.hello),
            "help": self._wrap_help(contact_commands.help),
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
            "add-note": self._wrap_note(note_commands.add_note),
            "show-notes": self._wrap_note(note_commands.show_notes),
            "edit-note": self._wrap_note(note_commands.edit_note),
            "delete-note": self._wrap_note(note_commands.delete_note),
            "add-tag": self._wrap_note(note_commands.add_tag),
            "remove-tag": self._wrap_note(note_commands.remove_tag),
            "search-notes": self._wrap_note(note_commands.search_notes),
            "search-by-tag": self._wrap_note(note_commands.search_by_tag),
        }

    def _wrap(self, command_func: Callable) -> Callable:
        @handle_errors
        def wrapper(args: List[str]) -> str:
            return command_func(args, self.contact_service)
        return wrapper

    def _wrap_help(self, command_func: Callable) -> Callable:
        @handle_errors
        def wrapper(args: List[str]) -> str:
            return command_func(args, self.contact_service, self.nlp_mode)
        return wrapper

    def _wrap_note(self, command_func: Callable) -> Callable:
        @handle_errors
        def wrapper(args: List[str]) -> str:
            return command_func(args, self.note_service)
        return wrapper

    def handle(self, command: str, args: List[str]) -> str:
        if command in ("close", "exit"):
            return "exit"

        if command in self.commands:
            return self.commands[command](args)

        available = [*self.commands.keys(), "close", "exit"]
        suggestion = get_close_matches(command, available, n=1, cutoff=0.6)
        return UIMessages.invalid_command(available, suggestion[0] if suggestion else None)

    def get_available_commands(self) -> List[str]:
        return [*self.commands.keys(), "close", "exit"]

    def get_nlp_command_examples(self) -> List[str]:
        return [
            # Contact management
            "add a contact",
            "add contact with phone",
            "add contact with email and address",
            "change phone number",
            "delete a contact",
            "remove a contact",
            "show phone for contact",
            "show all contacts",
            "list all contacts",

            # Birthday commands
            "add birthday",
            "add birthday for contact",
            "show birthday",
            "show upcoming birthdays",
            "show birthdays for next week",

            # Email commands
            "add email",
            "add email to contact",
            "edit email",
            "change email",
            "remove email",
            "delete email",

            # Address commands
            "add address",
            "add address to contact",
            "edit address",
            "change address",
            "remove address",
            "delete address",

            # Search and find
            "search contacts",
            "search for contact",
            "find contact",
            "find by name",

            # Note commands
            "add a note",
            "create a note",
            "show my notes",
            "show all notes",
            "edit a note",
            "update a note",
            "delete a note",
            "remove a note",

            # Note tag commands
            "add tag to note",
            "add tag",
            "remove tag from note",
            "remove tag",
            "search notes",
            "search notes by text",
            "search notes by tag",
            "find notes with tag",

            # General commands
            "hello",
            "help",
            "save",
            "load",
            "exit",
            "close",
        ]
