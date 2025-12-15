import readline
from abc import ABC, abstractmethod
from difflib import get_close_matches
from typing import List, Optional, Callable, Dict, Any


class CompletionProvider(ABC):
    @abstractmethod
    def get_completions(self, text: str, state: int) -> Optional[str]:
        pass

    @abstractmethod
    def get_candidates(self, text: str) -> List[str]:
        pass


class CommandCompleter(CompletionProvider):
    def __init__(self, commands: List[str]):
        self.commands = sorted(commands)
        self._matches: List[str] = []

    def update_commands(self, commands: List[str]) -> None:
        self.commands = sorted(commands)

    def get_candidates(self, text: str) -> List[str]:
        if not text:
            return self.commands

        text_lower = text.lower()
        return [cmd for cmd in self.commands if cmd.lower().startswith(text_lower)]

    def get_completions(self, text: str, state: int) -> Optional[str]:
        if state == 0:
            self._matches = self.get_candidates(text)

        if state < len(self._matches):
            return self._matches[state]
        return None

    def suggest_closest(self, text: str, cutoff: float = 0.6) -> Optional[str]:
        matches = get_close_matches(text.lower(), self.commands, n=1, cutoff=cutoff)
        return matches[0] if matches else None


class ContextualCompleter(CompletionProvider):
    def __init__(
        self,
        commands: List[str],
        param_providers: Optional[Dict[str, Callable[[], List[str]]]] = None,
    ):
        self.command_completer = CommandCompleter(commands)
        self.param_providers = param_providers or {}
        self._current_command: Optional[str] = None
        self._current_param_idx: int = 0
        self._matches: List[str] = []

    def update_commands(self, commands: List[str]) -> None:
        self.command_completer.update_commands(commands)

    def register_param_provider(
        self, command: str, provider: Callable[[], List[str]]
    ) -> None:
        self.param_providers[command] = provider

    def get_candidates(self, text: str) -> List[str]:
        parts = text.split()

        if not parts or (len(parts) == 1 and not text.endswith(" ")):
            return self.command_completer.get_candidates(text)

        command = parts[0].lower()
        self._current_command = command

        if command in self.param_providers:
            candidates = self.param_providers[command]()
            if len(parts) > 1 and not text.endswith(" "):
                partial = parts[-1].lower()
                return [c for c in candidates if c.lower().startswith(partial)]
            return candidates

        return []

    def get_completions(self, text: str, state: int) -> Optional[str]:
        if state == 0:
            line = readline.get_line_buffer()
            self._matches = self.get_candidates(line)

        if state < len(self._matches):
            return self._matches[state]
        return None


class AutocompleteEngine:
    def __init__(self):
        self._completer: Optional[CompletionProvider] = None
        self._original_completer = None
        self._original_delims = None

    def setup(self, completer: CompletionProvider) -> None:
        self._completer = completer
        self._original_completer = readline.get_completer()
        self._original_delims = readline.get_completer_delims()

        readline.set_completer(self._complete)
        readline.set_completer_delims(" \t\n")
        readline.parse_and_bind("tab: complete")

    def _complete(self, text: str, state: int) -> Optional[str]:
        if self._completer:
            return self._completer.get_completions(text, state)
        return None

    def teardown(self) -> None:
        if self._original_completer is not None:
            readline.set_completer(self._original_completer)
        if self._original_delims is not None:
            readline.set_completer_delims(self._original_delims)

    def input_with_completion(self, prompt: str) -> str:
        try:
            return input(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            return ""

    def get_candidates_for_display(self, text: str) -> List[str]:
        if self._completer:
            return self._completer.get_candidates(text)
        return []


class SelectionCompleter(CompletionProvider):
    def __init__(self, options: List[str]):
        self.options = options
        self._matches: List[str] = []

    def get_candidates(self, text: str) -> List[str]:
        if not text:
            return self.options

        text_lower = text.lower()
        return [opt for opt in self.options if opt.lower().startswith(text_lower)]

    def get_completions(self, text: str, state: int) -> Optional[str]:
        if state == 0:
            self._matches = self.get_candidates(text)

        if state < len(self._matches):
            return self._matches[state]
        return None
