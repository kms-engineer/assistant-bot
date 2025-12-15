from difflib import SequenceMatcher
from typing import List, Optional, Callable, Dict, Iterable

from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style


def similarity_score(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


class RankedCompleter(Completer):
    def __init__(
        self,
        commands: List[str],
        param_providers: Optional[Dict[str, Callable[[], List[str]]]] = None,
    ):
        self._commands = sorted(commands)
        self._param_providers = param_providers or {}

    def update_commands(self, commands: List[str]) -> None:
        self._commands = sorted(commands)

    def register_param_provider(
        self, command: str, provider: Callable[[], List[str]]
    ) -> None:
        self._param_providers[command] = provider

    def get_completions(
        self, document: Document, complete_event
    ) -> Iterable[Completion]:
        text = document.text_before_cursor
        parts = text.split()

        if not parts or (len(parts) == 1 and not text.endswith(" ")):
            yield from self._complete_commands(text.strip())
        else:
            command = parts[0].lower()
            if command in self._param_providers:
                partial = parts[-1] if not text.endswith(" ") else ""
                yield from self._complete_params(command, partial)

    def _complete_commands(self, partial: str) -> Iterable[Completion]:
        if not partial:
            for cmd in self._commands:
                yield Completion(cmd, start_position=0)
            return

        partial_lower = partial.lower()
        scored = []

        for cmd in self._commands:
            cmd_lower = cmd.lower()
            if cmd_lower.startswith(partial_lower):
                score = 1.0 + len(partial) / len(cmd)
                scored.append((cmd, score))
            elif partial_lower in cmd_lower:
                score = 0.5 + similarity_score(partial, cmd)
                scored.append((cmd, score))
            else:
                sim = similarity_score(partial, cmd)
                if sim > 0.4:
                    scored.append((cmd, sim))

        scored.sort(key=lambda x: -x[1])

        for cmd, score in scored:
            display_meta = self._get_command_meta(cmd)
            yield Completion(
                cmd,
                start_position=-len(partial),
                display_meta=display_meta,
            )

    def _complete_params(self, command: str, partial: str) -> Iterable[Completion]:
        provider = self._param_providers.get(command)
        if not provider:
            return

        try:
            candidates = provider()
        except Exception:
            return

        if not partial:
            for cand in candidates[:20]:
                yield Completion(cand, start_position=0)
            return

        partial_lower = partial.lower()
        scored = []

        for cand in candidates:
            cand_lower = cand.lower()
            if cand_lower.startswith(partial_lower):
                score = 1.0 + len(partial) / len(cand)
                scored.append((cand, score))
            elif partial_lower in cand_lower:
                score = 0.5 + similarity_score(partial, cand)
                scored.append((cand, score))
            else:
                sim = similarity_score(partial, cand)
                if sim > 0.3:
                    scored.append((cand, sim))

        scored.sort(key=lambda x: -x[1])

        for cand, score in scored[:15]:
            yield Completion(cand, start_position=-len(partial))

    def _get_command_meta(self, cmd: str) -> str:
        meta_map = {
            "add": "Add contact",
            "add-note": "Add note",
            "search": "Search contacts",
            "find": "Find exact match",
            "help": "Show commands",
            "all": "Show all contacts",
            "notes": "Show all notes",
        }
        return meta_map.get(cmd, "")


class CommandAutoSuggest(AutoSuggest):
    def __init__(self, commands: List[str]):
        self._commands = commands

    def update_commands(self, commands: List[str]) -> None:
        self._commands = commands

    def get_suggestion(self, buffer: Buffer, document: Document) -> Optional[Suggestion]:
        text = document.text
        if not text or " " in text:
            return None

        text_lower = text.lower()
        for cmd in self._commands:
            if cmd.lower().startswith(text_lower) and cmd != text:
                return Suggestion(cmd[len(text):])

        return None


PROMPT_STYLE = Style.from_dict({
    "": "#ffffff",
    "prompt": "#5555ff bold",
    "completion-menu.completion": "bg:#333333 #ffffff",
    "completion-menu.completion.current": "bg:#00aaaa #000000",
    "completion-menu.meta.completion": "bg:#333333 #888888",
    "completion-menu.meta.completion.current": "bg:#00aaaa #444444",
    "auto-suggestion": "#666666",
})


def strip_ansi(text: str) -> str:
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


class PromptCompleterSession:
    def __init__(
        self,
        commands: List[str],
        param_providers: Optional[Dict[str, Callable[[], List[str]]]] = None,
    ):
        self._completer = RankedCompleter(commands, param_providers)
        self._auto_suggest = CommandAutoSuggest(commands)
        self._session = PromptSession(
            completer=self._completer,
            auto_suggest=self._auto_suggest,
            complete_while_typing=True,
            style=PROMPT_STYLE,
        )

    def update_commands(self, commands: List[str]) -> None:
        self._completer.update_commands(commands)
        self._auto_suggest.update_commands(commands)

    def register_param_provider(
        self, command: str, provider: Callable[[], List[str]]
    ) -> None:
        self._completer.register_param_provider(command, provider)

    def prompt(self, message: str = ">>> ") -> str:
        clean_message = strip_ansi(message)
        formatted = [("class:prompt", clean_message)]
        return self._session.prompt(formatted)
