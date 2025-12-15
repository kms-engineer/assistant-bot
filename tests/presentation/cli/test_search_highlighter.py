import pytest
from colorama import Fore, Back, Style

from src.presentation.cli.search_highlighter import SearchHighlighter


class TestSearchHighlighter:

    def test_highlight_single_term(self):
        highlighter = SearchHighlighter()
        highlighter.set_search_term("test")
        result = highlighter.highlight("This is a test string")

        assert Back.YELLOW in result
        assert Style.RESET_ALL in result

    def test_highlight_case_insensitive(self):
        highlighter = SearchHighlighter(case_sensitive=False)
        highlighter.set_search_term("TEST")
        result = highlighter.highlight("This is a test string")

        assert Back.YELLOW in result

    def test_highlight_case_sensitive(self):
        highlighter = SearchHighlighter(case_sensitive=True)
        highlighter.set_search_term("TEST")
        result = highlighter.highlight("This is a test string")

        assert Back.YELLOW not in result

    def test_highlight_multiple_terms(self):
        highlighter = SearchHighlighter()
        highlighter.set_search_terms(["hello", "world"])
        result = highlighter.highlight("hello beautiful world")

        assert result.count(Back.YELLOW) == 2

    def test_highlight_no_match(self):
        highlighter = SearchHighlighter()
        highlighter.set_search_term("xyz")
        text = "This is a test"
        result = highlighter.highlight(text)

        assert Back.YELLOW not in result
        assert text in result

    def test_highlight_empty_term(self):
        highlighter = SearchHighlighter()
        highlighter.set_search_term("")
        text = "This is a test"
        result = highlighter.highlight(text)

        assert result == text

    def test_highlight_empty_text(self):
        highlighter = SearchHighlighter()
        highlighter.set_search_term("test")
        result = highlighter.highlight("")

        assert result == ""

    def test_contains_match_true(self):
        highlighter = SearchHighlighter()
        highlighter.set_search_term("test")

        assert highlighter.contains_match("This is a test") is True

    def test_contains_match_false(self):
        highlighter = SearchHighlighter()
        highlighter.set_search_term("xyz")

        assert highlighter.contains_match("This is a test") is False

    def test_contains_match_case_insensitive(self):
        highlighter = SearchHighlighter(case_sensitive=False)
        highlighter.set_search_term("TEST")

        assert highlighter.contains_match("This is a test") is True

    def test_highlight_in_context(self):
        highlighter = SearchHighlighter()
        highlighter.set_search_term("important")
        text = "This is a very long text with an important word in the middle of it"
        result = highlighter.highlight_in_context(text, context_chars=10)

        assert "important" in result
        assert "..." in result

    def test_highlight_in_context_no_match(self):
        highlighter = SearchHighlighter()
        highlighter.set_search_term("xyz")
        text = "This is a test"
        result = highlighter.highlight_in_context(text)

        assert result == text

    def test_create_column_highlighter(self):
        highlighter = SearchHighlighter()
        highlighter.set_search_term("test")
        col_highlighter = highlighter.create_column_highlighter([0, 2])

        result_col0 = col_highlighter("test value", 0)
        result_col1 = col_highlighter("test value", 1)
        result_col2 = col_highlighter("test value", 2)

        assert Back.YELLOW in result_col0
        assert Back.YELLOW not in result_col1
        assert Back.YELLOW in result_col2

    def test_create_column_highlighter_all_columns(self):
        highlighter = SearchHighlighter()
        highlighter.set_search_term("test")
        col_highlighter = highlighter.create_column_highlighter(None)

        result = col_highlighter("test value", 5)
        assert Back.YELLOW in result

    def test_custom_colors(self):
        highlighter = SearchHighlighter(
            highlight_fg=Fore.WHITE,
            highlight_bg=Back.RED,
        )
        highlighter.set_search_term("test")
        result = highlighter.highlight("This is a test")

        assert Back.RED in result
        assert Fore.WHITE in result

    def test_special_regex_characters(self):
        highlighter = SearchHighlighter()
        highlighter.set_search_term("[test]")
        result = highlighter.highlight("This is [test] with brackets")

        assert Back.YELLOW in result

    def test_multiple_occurrences(self):
        highlighter = SearchHighlighter()
        highlighter.set_search_term("a")
        result = highlighter.highlight("a banana")

        assert result.count(Back.YELLOW) == 4
