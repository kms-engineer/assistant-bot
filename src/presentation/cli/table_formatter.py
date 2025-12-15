from typing import List, Dict, Any, Optional, Callable


class TableFormatter:
    DEFAULT_MIN_WIDTH = 3
    DEFAULT_MAX_WIDTH = 50
    ELLIPSIS = "..."

    def __init__(
        self,
        headers: List[str],
        min_col_width: int = DEFAULT_MIN_WIDTH,
        max_col_width: int = DEFAULT_MAX_WIDTH,
        show_borders: bool = True,
    ):
        self.headers = headers
        self.min_col_width = min_col_width
        self.max_col_width = max_col_width
        self.show_borders = show_borders
        self._col_widths: List[int] = []

    def format(
        self,
        rows: List[List[Any]],
        highlighter: Optional[Callable[[str, int], str]] = None,
    ) -> str:
        if not rows:
            return "No data to display."

        str_rows = [[str(cell) for cell in row] for row in rows]
        self._calculate_widths(str_rows)

        lines = []

        if self.show_borders:
            lines.append(self._build_separator())

        lines.append(self._build_header_row())

        if self.show_borders:
            lines.append(self._build_separator())

        for row_idx, row in enumerate(str_rows):
            lines.append(self._build_data_row(row, row_idx, highlighter))

        if self.show_borders:
            lines.append(self._build_separator())

        return "\n".join(lines)

    def _calculate_widths(self, rows: List[List[str]]) -> None:
        self._col_widths = [len(h) for h in self.headers]

        for row in rows:
            for i, cell in enumerate(row):
                if i < len(self._col_widths):
                    self._col_widths[i] = max(self._col_widths[i], len(cell))

        self._col_widths = [
            max(self.min_col_width, min(w, self.max_col_width))
            for w in self._col_widths
        ]

    def _truncate(self, text: str, width: int) -> str:
        if len(text) <= width:
            return text
        return text[: width - len(self.ELLIPSIS)] + self.ELLIPSIS

    def _build_separator(self) -> str:
        parts = ["-" * w for w in self._col_widths]
        return "+-" + "-+-".join(parts) + "-+"

    def _build_header_row(self) -> str:
        cells = []
        for i, header in enumerate(self.headers):
            width = self._col_widths[i] if i < len(self._col_widths) else len(header)
            truncated = self._truncate(header, width)
            cells.append(truncated.ljust(width))

        if self.show_borders:
            return "| " + " | ".join(cells) + " |"
        return "  ".join(cells)

    def _build_data_row(
        self,
        row: List[str],
        row_idx: int,
        highlighter: Optional[Callable[[str, int], str]] = None,
    ) -> str:
        cells = []
        for i, cell in enumerate(row):
            width = self._col_widths[i] if i < len(self._col_widths) else len(cell)
            truncated = self._truncate(cell, width)

            if highlighter:
                displayed = highlighter(truncated, i)
                padding = width - len(truncated)
                displayed = displayed + " " * padding
            else:
                displayed = truncated.ljust(width)

            cells.append(displayed)

        if self.show_borders:
            return "| " + " | ".join(cells) + " |"
        return "  ".join(cells)

    @classmethod
    def from_dicts(
        cls,
        data: List[Dict[str, Any]],
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> "TableFormatter":
        if not data:
            return cls(headers=columns or [], **kwargs)

        if columns is None:
            columns = list(data[0].keys())

        return cls(headers=columns, **kwargs)

    @classmethod
    def format_dicts(
        cls,
        data: List[Dict[str, Any]],
        columns: Optional[List[str]] = None,
        highlighter: Optional[Callable[[str, int], str]] = None,
        **kwargs,
    ) -> str:
        if not data:
            return "No data to display."

        if columns is None:
            columns = list(data[0].keys())

        formatter = cls(headers=columns, **kwargs)
        rows = [[item.get(col, "") for col in columns] for item in data]
        return formatter.format(rows, highlighter)
