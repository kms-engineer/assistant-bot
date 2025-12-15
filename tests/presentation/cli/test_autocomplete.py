import pytest
from unittest.mock import patch, MagicMock

from src.presentation.cli.autocomplete import (
    CommandCompleter,
    ContextualCompleter,
    AutocompleteEngine,
    SelectionCompleter,
)


class TestCommandCompleter:

    def test_get_candidates_empty_text(self):
        completer = CommandCompleter(["add", "delete", "search"])
        candidates = completer.get_candidates("")

        assert candidates == ["add", "delete", "search"]

    def test_get_candidates_partial_match(self):
        completer = CommandCompleter(["add", "add-note", "delete"])
        candidates = completer.get_candidates("add")

        assert "add" in candidates
        assert "add-note" in candidates
        assert "delete" not in candidates

    def test_get_candidates_case_insensitive(self):
        completer = CommandCompleter(["Add", "Delete"])
        candidates = completer.get_candidates("a")

        assert "Add" in candidates

    def test_get_candidates_no_match(self):
        completer = CommandCompleter(["add", "delete"])
        candidates = completer.get_candidates("xyz")

        assert candidates == []

    def test_get_completions_iteration(self):
        completer = CommandCompleter(["add", "add-note"])

        first = completer.get_completions("add", 0)
        second = completer.get_completions("add", 1)
        third = completer.get_completions("add", 2)

        assert first == "add"
        assert second == "add-note"
        assert third is None

    def test_update_commands(self):
        completer = CommandCompleter(["old"])
        completer.update_commands(["new", "commands"])
        candidates = completer.get_candidates("")

        assert "old" not in candidates
        assert "commands" in candidates
        assert "new" in candidates

    def test_suggest_closest(self):
        completer = CommandCompleter(["add", "delete", "search"])
        suggestion = completer.suggest_closest("ad")

        assert suggestion == "add"

    def test_suggest_closest_no_match(self):
        completer = CommandCompleter(["add", "delete"])
        suggestion = completer.suggest_closest("xyz", cutoff=0.8)

        assert suggestion is None


class TestContextualCompleter:

    def test_command_completion(self):
        completer = ContextualCompleter(["add", "delete"])
        candidates = completer.get_candidates("a")

        assert "add" in candidates
        assert "delete" not in candidates

    def test_param_completion(self):
        completer = ContextualCompleter(
            commands=["add"],
            param_providers={"add": lambda: ["Alice", "Bob", "Charlie"]},
        )
        candidates = completer.get_candidates("add ")

        assert "Alice" in candidates
        assert "Bob" in candidates

    def test_param_completion_partial(self):
        completer = ContextualCompleter(
            commands=["add"],
            param_providers={"add": lambda: ["Alice", "Bob"]},
        )
        candidates = completer.get_candidates("add A")

        assert "Alice" in candidates
        assert "Bob" not in candidates

    def test_register_param_provider(self):
        completer = ContextualCompleter(commands=["search"])
        completer.register_param_provider("search", lambda: ["John", "Jane"])
        candidates = completer.get_candidates("search ")

        assert "John" in candidates
        assert "Jane" in candidates


class TestSelectionCompleter:

    def test_get_candidates_all(self):
        completer = SelectionCompleter(["Option 1", "Option 2", "Option 3"])
        candidates = completer.get_candidates("")

        assert len(candidates) == 3

    def test_get_candidates_filtered(self):
        completer = SelectionCompleter(["Apple", "Banana", "Avocado"])
        candidates = completer.get_candidates("A")

        assert "Apple" in candidates
        assert "Avocado" in candidates
        assert "Banana" not in candidates

    def test_get_completions(self):
        completer = SelectionCompleter(["Yes", "No"])

        first = completer.get_completions("", 0)
        second = completer.get_completions("", 1)
        third = completer.get_completions("", 2)

        assert first == "Yes"
        assert second == "No"
        assert third is None


class TestAutocompleteEngine:

    @patch("src.presentation.cli.autocomplete.readline")
    def test_setup_configures_readline(self, mock_readline):
        engine = AutocompleteEngine()
        completer = CommandCompleter(["test"])
        engine.setup(completer)

        mock_readline.set_completer.assert_called()
        mock_readline.parse_and_bind.assert_called_with("tab: complete")

    @patch("src.presentation.cli.autocomplete.readline")
    def test_teardown_restores_readline(self, mock_readline):
        mock_readline.get_completer.return_value = None
        mock_readline.get_completer_delims.return_value = " "

        engine = AutocompleteEngine()
        completer = CommandCompleter(["test"])
        engine.setup(completer)
        engine.teardown()

        assert mock_readline.set_completer.call_count >= 1

    def test_get_candidates_for_display(self):
        engine = AutocompleteEngine()
        completer = CommandCompleter(["add", "delete"])
        engine.setup(completer)

        candidates = engine.get_candidates_for_display("a")
        assert "add" in candidates

    def test_get_candidates_without_completer(self):
        engine = AutocompleteEngine()
        candidates = engine.get_candidates_for_display("test")

        assert candidates == []
