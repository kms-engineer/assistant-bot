import re
from typing import List, Optional
from colorama import Fore, Back, Style


class SearchHighlighter:
    def __init__(
        self,
        highlight_fg: str = Fore.BLACK,
        highlight_bg: str = Back.YELLOW,
        case_sensitive: bool = False,
    ):
        self.highlight_fg = highlight_fg
        self.highlight_bg = highlight_bg
        self.case_sensitive = case_sensitive
        self._search_terms: List[str] = []

    def set_search_terms(self, terms: List[str]) -> None:
        self._search_terms = [t for t in terms if t]

    def set_search_term(self, term: str) -> None:
        self._search_terms = [term] if term else []

    def highlight(self, text: str) -> str:
        if not self._search_terms or not text:
            return text

        result = text
        for term in self._search_terms:
            result = self._highlight_term(result, term)

        return result

    def _highlight_term(self, text: str, term: str) -> str:
        if not term:
            return text

        flags = 0 if self.case_sensitive else re.IGNORECASE
        pattern = re.compile(re.escape(term), flags)

        def replacer(match: re.Match) -> str:
            matched_text = match.group(0)
            return (
                f"{self.highlight_bg}{self.highlight_fg}"
                f"{matched_text}"
                f"{Style.RESET_ALL}"
            )

        return pattern.sub(replacer, text)

    def highlight_in_context(
        self,
        text: str,
        context_chars: int = 30,
        max_matches: int = 3,
    ) -> str:
        if not self._search_terms or not text:
            return text

        matches_info = []
        for term in self._search_terms:
            flags = 0 if self.case_sensitive else re.IGNORECASE
            pattern = re.compile(re.escape(term), flags)
            for match in pattern.finditer(text):
                matches_info.append((match.start(), match.end(), match.group(0)))

        if not matches_info:
            return text

        matches_info.sort(key=lambda x: x[0])
        matches_info = matches_info[:max_matches]

        snippets = []
        for start, end, matched in matches_info:
            ctx_start = max(0, start - context_chars)
            ctx_end = min(len(text), end + context_chars)

            prefix = "..." if ctx_start > 0 else ""
            suffix = "..." if ctx_end < len(text) else ""

            before = text[ctx_start:start]
            after = text[end:ctx_end]
            highlighted = (
                f"{self.highlight_bg}{self.highlight_fg}"
                f"{matched}"
                f"{Style.RESET_ALL}"
            )

            snippets.append(f"{prefix}{before}{highlighted}{after}{suffix}")

        return " | ".join(snippets)

    def contains_match(self, text: str) -> bool:
        if not self._search_terms or not text:
            return False

        for term in self._search_terms:
            flags = 0 if self.case_sensitive else re.IGNORECASE
            if re.search(re.escape(term), text, flags):
                return True

        return False

    def create_column_highlighter(self, columns_to_highlight: Optional[List[int]] = None):
        def highlighter(text: str, col_idx: int) -> str:
            if columns_to_highlight is None or col_idx in columns_to_highlight:
                return self.highlight(text)
            return text

        return highlighter
