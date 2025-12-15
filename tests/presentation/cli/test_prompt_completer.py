import pytest
from unittest.mock import MagicMock

from prompt_toolkit.document import Document

from src.presentation.cli.prompt_completer import (
    RankedCompleter,
    CommandAutoSuggest,
    similarity_score,
)


class TestSimilarityScore:

    def test_identical_strings(self):
        score = similarity_score("hello", "hello")
        assert score == 1.0

    def test_different_strings(self):
        score = similarity_score("hello", "world")
        assert score < 0.5

    def test_similar_strings(self):
        score = similarity_score("add", "ad")
        assert score > 0.6

    def test_case_insensitive(self):
        score = similarity_score("Hello", "hello")
        assert score == 1.0


class TestRankedCompleter:

    def test_complete_commands_empty_input(self):
        completer = RankedCompleter(commands=["add", "delete", "search"])
        doc = Document("")

        completions = list(completer.get_completions(doc, None))

        assert len(completions) == 3

    def test_complete_commands_prefix_match(self):
        completer = RankedCompleter(commands=["add", "add-note", "delete"])
        doc = Document("ad")

        completions = list(completer.get_completions(doc, None))

        assert len(completions) >= 2
        texts = [c.text for c in completions]
        assert "add" in texts
        assert "add-note" in texts

    def test_complete_commands_ranked_by_relevance(self):
        completer = RankedCompleter(commands=["add", "add-note", "delete"])
        doc = Document("add")

        completions = list(completer.get_completions(doc, None))

        assert completions[0].text == "add"
        assert completions[1].text == "add-note"

    def test_complete_params_after_command(self):
        def contact_provider():
            return ["Alice", "Bob", "Charlie"]

        completer = RankedCompleter(
            commands=["search"],
            param_providers={"search": contact_provider},
        )
        doc = Document("search ")

        completions = list(completer.get_completions(doc, None))

        texts = [c.text for c in completions]
        assert "Alice" in texts
        assert "Bob" in texts

    def test_complete_params_with_partial(self):
        def contact_provider():
            return ["Alice", "Bob", "Alex"]

        completer = RankedCompleter(
            commands=["search"],
            param_providers={"search": contact_provider},
        )
        doc = Document("search Al")

        completions = list(completer.get_completions(doc, None))

        texts = [c.text for c in completions]
        assert "Alice" in texts
        assert "Alex" in texts
        assert "Bob" not in texts

    def test_update_commands(self):
        completer = RankedCompleter(commands=["old"])
        completer.update_commands(["new", "commands"])

        doc = Document("n")
        completions = list(completer.get_completions(doc, None))

        texts = [c.text for c in completions]
        assert "new" in texts

    def test_register_param_provider(self):
        completer = RankedCompleter(commands=["test"])
        completer.register_param_provider("test", lambda: ["param1", "param2"])

        doc = Document("test ")
        completions = list(completer.get_completions(doc, None))

        texts = [c.text for c in completions]
        assert "param1" in texts

    def test_fuzzy_match(self):
        completer = RankedCompleter(commands=["delete-contact", "delete-note"])
        doc = Document("delcon")

        completions = list(completer.get_completions(doc, None))

        texts = [c.text for c in completions]
        assert "delete-contact" in texts


class TestCommandAutoSuggest:

    def test_suggest_matching_command(self):
        suggestor = CommandAutoSuggest(commands=["add", "delete", "search"])
        doc = Document("ad")
        buffer = MagicMock()

        suggestion = suggestor.get_suggestion(buffer, doc)

        assert suggestion is not None
        assert suggestion.text == "d"

    def test_no_suggestion_for_complete_command(self):
        suggestor = CommandAutoSuggest(commands=["add", "delete"])
        doc = Document("add")
        buffer = MagicMock()

        suggestion = suggestor.get_suggestion(buffer, doc)

        assert suggestion is None

    def test_no_suggestion_with_space(self):
        suggestor = CommandAutoSuggest(commands=["add", "delete"])
        doc = Document("add arg")
        buffer = MagicMock()

        suggestion = suggestor.get_suggestion(buffer, doc)

        assert suggestion is None

    def test_no_suggestion_for_empty(self):
        suggestor = CommandAutoSuggest(commands=["add"])
        doc = Document("")
        buffer = MagicMock()

        suggestion = suggestor.get_suggestion(buffer, doc)

        assert suggestion is None

    def test_update_commands(self):
        suggestor = CommandAutoSuggest(commands=["old"])
        suggestor.update_commands(["new-command"])

        doc = Document("new")
        buffer = MagicMock()
        suggestion = suggestor.get_suggestion(buffer, doc)

        assert suggestion is not None
        assert suggestion.text == "-command"
