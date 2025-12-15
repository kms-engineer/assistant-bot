from dataclasses import dataclass, field
from typing import List, Optional, Callable, Dict, Any
from colorama import Fore, Style

from src.presentation.cli.autocomplete import (
    AutocompleteEngine,
    SelectionCompleter,
)


@dataclass
class InputField:
    name: str
    prompt: str
    required: bool = True
    validator: Optional[Callable[[str], bool]] = None
    error_message: str = "Invalid input"
    completer_options: Optional[List[str]] = None
    default: Optional[str] = None
    transform: Optional[Callable[[str], Any]] = None


@dataclass
class InputResult:
    success: bool
    values: Dict[str, Any] = field(default_factory=dict)
    cancelled: bool = False
    error: Optional[str] = None


class InteractiveInputBuilder:
    OPTIONAL_MARKER = "(optional)"
    SKIP_HINT = "Press Enter to skip"
    CANCEL_COMMANDS = {"cancel", "quit", "exit", "q"}

    def __init__(self):
        self._fields: List[InputField] = []
        self._autocomplete = AutocompleteEngine()
        self._show_progress = True
        self._allow_cancel = True

    def add_field(
        self,
        name: str,
        prompt: str,
        required: bool = True,
        validator: Optional[Callable[[str], bool]] = None,
        error_message: str = "Invalid input",
        completer_options: Optional[List[str]] = None,
        default: Optional[str] = None,
        transform: Optional[Callable[[str], Any]] = None,
    ) -> "InteractiveInputBuilder":
        self._fields.append(
            InputField(
                name=name,
                prompt=prompt,
                required=required,
                validator=validator,
                error_message=error_message,
                completer_options=completer_options,
                default=default,
                transform=transform,
            )
        )
        return self

    def show_progress(self, show: bool) -> "InteractiveInputBuilder":
        self._show_progress = show
        return self

    def allow_cancel(self, allow: bool) -> "InteractiveInputBuilder":
        self._allow_cancel = allow
        return self

    def build(self) -> InputResult:
        values: Dict[str, Any] = {}
        total = len(self._fields)

        for idx, field_spec in enumerate(self._fields, 1):
            result = self._collect_field(field_spec, idx, total)

            if result.cancelled:
                return InputResult(success=False, cancelled=True)

            if result.error:
                return InputResult(success=False, error=result.error)

            if field_spec.name in result.values:
                values[field_spec.name] = result.values[field_spec.name]

        return InputResult(success=True, values=values)

    def _collect_field(
        self, field_spec: InputField, current: int, total: int
    ) -> InputResult:
        prompt = self._build_prompt(field_spec, current, total)

        if field_spec.completer_options:
            completer = SelectionCompleter(field_spec.completer_options)
            self._autocomplete.setup(completer)

        try:
            while True:
                try:
                    value = input(prompt).strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    return InputResult(success=False, cancelled=True)

                if self._allow_cancel and value.lower() in self.CANCEL_COMMANDS:
                    return InputResult(success=False, cancelled=True)

                if not value:
                    if not field_spec.required:
                        if field_spec.default is not None:
                            value = field_spec.default
                        else:
                            return InputResult(success=True, values={})
                    else:
                        print(
                            f"{Fore.RED}This field is required.{Style.RESET_ALL}"
                        )
                        continue

                if field_spec.validator and not field_spec.validator(value):
                    print(f"{Fore.RED}{field_spec.error_message}{Style.RESET_ALL}")
                    continue

                final_value = value
                if field_spec.transform:
                    try:
                        final_value = field_spec.transform(value)
                    except Exception as e:
                        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                        continue

                return InputResult(
                    success=True, values={field_spec.name: final_value}
                )

        finally:
            if field_spec.completer_options:
                self._autocomplete.teardown()

    def _build_prompt(
        self, field_spec: InputField, current: int, total: int
    ) -> str:
        parts = []

        if self._show_progress:
            progress = f"[{current}/{total}] "
            parts.append(progress)

        parts.append(field_spec.prompt)

        if not field_spec.required:
            parts.append(f" {self.OPTIONAL_MARKER}")

        if field_spec.default is not None:
            parts.append(f" [{field_spec.default}]")

        parts.append(": ")

        return "".join(parts)

    def reset(self) -> "InteractiveInputBuilder":
        self._fields = []
        return self


class QuickInput:
    @staticmethod
    def confirm(prompt: str, default: bool = False) -> bool:
        hint = "[Y/n]" if default else "[y/N]"
        full_prompt = f"{prompt} {hint}: "

        try:
            response = input(full_prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return False

        if not response:
            return default

        return response in ("y", "yes")

    @staticmethod
    def select(
        prompt: str,
        options: List[str],
        allow_cancel: bool = True,
    ) -> Optional[int]:
        print(f"\n{prompt}")
        for idx, option in enumerate(options, 1):
            print(f"  {idx}. {option}")

        if allow_cancel:
            print("  0. Cancel")

        while True:
            try:
                choice = input("\nEnter choice: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return None

            if not choice:
                continue

            try:
                num = int(choice)
                if num == 0 and allow_cancel:
                    return None
                if 1 <= num <= len(options):
                    return num - 1
            except ValueError:
                pass

            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

    @staticmethod
    def text(
        prompt: str,
        required: bool = True,
        validator: Optional[Callable[[str], bool]] = None,
        error_message: str = "Invalid input",
    ) -> Optional[str]:
        suffix = "" if required else " (optional)"
        full_prompt = f"{prompt}{suffix}: "

        while True:
            try:
                value = input(full_prompt).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return None

            if not value:
                if not required:
                    return None
                print(f"{Fore.RED}This field is required.{Style.RESET_ALL}")
                continue

            if validator and not validator(value):
                print(f"{Fore.RED}{error_message}{Style.RESET_ALL}")
                continue

            return value
