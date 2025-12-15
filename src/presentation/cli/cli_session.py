from difflib import get_close_matches
from typing import List, Optional, Callable, Dict

from src.application.services.contact_service import ContactService
from src.application.services.note_service import NoteService
from src.presentation.cli.prompt_completer import PromptCompleterSession
from src.presentation.cli.selection import select_from_list


class CLISession:
    SUGGESTION_CUTOFF = 0.6

    def __init__(
        self,
        commands: List[str],
        contact_service: Optional[ContactService] = None,
        note_service: Optional[NoteService] = None,
        use_prompt_toolkit: bool = True,
    ):
        self._commands = sorted(commands)
        self._contact_service = contact_service
        self._note_service = note_service
        self._use_prompt_toolkit = use_prompt_toolkit
        self._prompt_session: Optional[PromptCompleterSession] = None
        self._setup_completer()

    def _setup_completer(self) -> None:
        if not self._use_prompt_toolkit:
            return

        param_providers = self._build_param_providers()
        self._prompt_session = PromptCompleterSession(
            commands=self._commands,
            param_providers=param_providers,
        )

    def _build_param_providers(self) -> Dict[str, Callable[[], List[str]]]:
        providers: Dict[str, Callable[[], List[str]]] = {}

        if self._contact_service:
            providers.update({
                "add": self._get_contact_names,
                "change": self._get_contact_names,
                "delete-contact": self._get_contact_names,
                "delete-phone": self._get_contact_names,
                "delete-email": self._get_contact_names,
                "delete-address": self._get_contact_names,
                "delete-birthday": self._get_contact_names,
                "phone": self._get_contact_names,
                "add-birthday": self._get_contact_names,
                "show-birthday": self._get_contact_names,
                "add-email": self._get_contact_names,
                "change-email": self._get_contact_names,
                "add-address": self._get_contact_names,
                "change-address": self._get_contact_names,
                "search": self._get_search_suggestions,
                "find": self._get_search_suggestions,
            })

        if self._note_service:
            providers.update({
                "show-note": self._get_note_ids,
                "change-note": self._get_note_ids,
                "change-note-title": self._get_note_ids,
                "delete-note": self._get_note_ids,
                "add-tag": self._get_note_ids,
                "delete-tag": self._get_note_ids,
                "search-notes-by-tag": self._get_tags,
                "delete-note-by-tag": self._get_tags,
            })

        return providers

    def _get_contact_names(self) -> List[str]:
        if not self._contact_service:
            return []
        try:
            contacts = self._contact_service.get_all_contacts()
            return sorted(set(c.name.value for c in contacts))
        except Exception:
            return []

    def _get_search_suggestions(self) -> List[str]:
        if not self._contact_service:
            return []
        try:
            contacts = self._contact_service.get_all_contacts()
            suggestions = set()
            for c in contacts:
                suggestions.add(c.name.value)
                if c.email:
                    suggestions.add(c.email.value)
                for phone in c.phones:
                    suggestions.add(phone.value)
            return sorted(suggestions)
        except Exception:
            return []

    def _get_note_ids(self) -> List[str]:
        if not self._note_service:
            return []
        try:
            notes = self._note_service.get_all_notes()
            return [note.id for note in notes]
        except Exception:
            return []

    def _get_tags(self) -> List[str]:
        if not self._note_service:
            return []
        try:
            tags_dict = self._note_service.list_tags()
            return sorted(tags_dict.keys())
        except Exception:
            return []

    def update_commands(self, commands: List[str]) -> None:
        self._commands = sorted(commands)
        if self._prompt_session:
            self._prompt_session.update_commands(self._commands)

    def input(self, prompt: str = ">>> ") -> str:
        try:
            if self._prompt_session:
                return self._prompt_session.prompt(prompt).strip()
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            raise

    def validate_command(self, command: str) -> Optional[str]:
        if command in self._commands or command in ("close", "exit"):
            return None

        suggestion = self._suggest_command(command)
        return suggestion

    def _suggest_command(self, command: str) -> Optional[str]:
        all_commands = self._commands + ["close", "exit"]
        matches = get_close_matches(
            command.lower(),
            all_commands,
            n=1,
            cutoff=self.SUGGESTION_CUTOFF,
        )
        return matches[0] if matches else None

    def get_matching_commands(self, prefix: str) -> List[str]:
        if not prefix:
            return self._commands
        prefix_lower = prefix.lower()
        return [cmd for cmd in self._commands if cmd.lower().startswith(prefix_lower)]

    def select_command(self, matches: List[str]) -> Optional[str]:
        if not matches:
            return None

        if len(matches) == 1:
            return matches[0]

        print("\nMultiple commands match:")
        selected_idx = select_from_list(
            items=matches,
            prompt="Select command",
            formatter=lambda x: x,
            allow_cancel=True,
        )

        if selected_idx is None:
            return None

        return matches[selected_idx]

    def show_suggestion(self, invalid_command: str, suggestion: Optional[str]) -> None:
        if suggestion:
            print(f"Unknown command '{invalid_command}'. Did you mean '{suggestion}'?")
        else:
            print(f"Unknown command '{invalid_command}'. Type 'help' for available commands.")

    def show_instant_suggestions(self, partial: str) -> None:
        pass

    def teardown(self) -> None:
        pass


def create_cli_session(
    handler,
    contact_service: Optional[ContactService] = None,
    note_service: Optional[NoteService] = None,
    use_prompt_toolkit: bool = True,
) -> CLISession:
    commands = handler.get_available_commands()
    return CLISession(
        commands=commands,
        contact_service=contact_service,
        note_service=note_service,
        use_prompt_toolkit=use_prompt_toolkit,
    )
