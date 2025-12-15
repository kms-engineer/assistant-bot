import pytest
from colorama import Fore, Style

from src.presentation.cli.table_formatter import TableFormatter


class TestTableFormatter:

    def test_format_basic_table(self):
        formatter = TableFormatter(headers=["Name", "Phone"])
        rows = [["Alice", "123-456"], ["Bob", "789-012"]]
        result = formatter.format(rows)

        assert "Name" in result
        assert "Phone" in result
        assert "Alice" in result
        assert "Bob" in result

    def test_format_empty_rows(self):
        formatter = TableFormatter(headers=["Name", "Phone"])
        result = formatter.format([])

        assert result == "No data to display."

    def test_format_with_borders(self):
        formatter = TableFormatter(headers=["Name"], show_borders=True)
        rows = [["Alice"]]
        result = formatter.format(rows)

        assert "|" in result
        assert "+" in result
        assert "-" in result

    def test_format_without_borders(self):
        formatter = TableFormatter(headers=["Name"], show_borders=False)
        rows = [["Alice"]]
        result = formatter.format(rows)

        assert "|" not in result
        assert "+" not in result

    def test_truncate_long_text(self):
        formatter = TableFormatter(headers=["Name"], max_col_width=10)
        rows = [["This is a very long name that should be truncated"]]
        result = formatter.format(rows)

        assert "..." in result
        assert len("This is a very long name that should be truncated") > 10

    def test_column_width_respects_header(self):
        formatter = TableFormatter(headers=["LongHeaderName"])
        rows = [["X"]]
        result = formatter.format(rows)

        assert "LongHeaderName" in result

    def test_format_dicts_basic(self):
        data = [
            {"name": "Alice", "phone": "123"},
            {"name": "Bob", "phone": "456"},
        ]
        result = TableFormatter.format_dicts(data)

        assert "Alice" in result
        assert "Bob" in result
        assert "123" in result
        assert "456" in result

    def test_format_dicts_with_columns(self):
        data = [
            {"name": "Alice", "phone": "123", "email": "a@b.c"},
        ]
        result = TableFormatter.format_dicts(data, columns=["name", "phone"])

        assert "Alice" in result
        assert "123" in result
        assert "a@b.c" not in result

    def test_format_dicts_empty(self):
        result = TableFormatter.format_dicts([])

        assert result == "No data to display."

    def test_format_with_highlighter(self):
        formatter = TableFormatter(headers=["Name", "Phone"])
        rows = [["Alice", "123"]]

        def mock_highlighter(text, col_idx):
            if col_idx == 0:
                return f"[{text}]"
            return text

        result = formatter.format(rows, highlighter=mock_highlighter)
        assert "[Alice" in result

    def test_min_col_width(self):
        formatter = TableFormatter(headers=["A"], min_col_width=10)
        rows = [["X"]]
        result = formatter.format(rows)

        lines = result.split("\n")
        separator_line = lines[0]
        assert len(separator_line) > 10

    def test_multiple_columns(self):
        formatter = TableFormatter(headers=["Col1", "Col2", "Col3"])
        rows = [["A", "B", "C"], ["D", "E", "F"]]
        result = formatter.format(rows)

        assert "Col1" in result
        assert "Col2" in result
        assert "Col3" in result
        assert "A" in result
        assert "F" in result

    def test_special_characters_in_data(self):
        formatter = TableFormatter(headers=["Name"])
        rows = [["Test@#$%"]]
        result = formatter.format(rows)

        assert "Test@#$%" in result

    def test_unicode_characters(self):
        formatter = TableFormatter(headers=["Name"])
        rows = [["Caf\u00e9"]]  # Café with Unicode
        result = formatter.format(rows)

        assert "Name" in result
        assert "Caf\u00e9" in result
