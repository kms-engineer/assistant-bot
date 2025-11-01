import pytest
import re
from src.config.regex_patterns import RegexPatterns


class TestRegexPatterns:
    """Tests for the RegexPatterns class."""

    def test_all_patterns_are_valid_regex(self):
        """Test that all defined patterns are valid regular expressions."""
        for attr_name in dir(RegexPatterns):
            if attr_name.endswith("_PATTERN") or attr_name.endswith("_PATTERNS"):
                pattern_or_list = getattr(RegexPatterns, attr_name)
                if isinstance(pattern_or_list, list):
                    for i, pattern in enumerate(pattern_or_list):
                        try:
                            re.compile(pattern)
                        except re.error as e:
                            pytest.fail(f"Invalid regex in {attr_name}[{i}]: {pattern}\n{e}")
                elif isinstance(pattern_or_list, str):
                    try:
                        re.compile(pattern_or_list)
                    except re.error as e:
                        pytest.fail(f"Invalid regex in {attr_name}: {pattern_or_list}\n{e}")

    def test_placeholder_patterns(self):
        """Test patterns that require placeholder replacement."""
        # Test ADDRESS_CITY_STATE_ZIP_PATTERN
        state_pattern = "(?:AL|AK|AZ)"
        filled_pattern = RegexPatterns.ADDRESS_CITY_STATE_ZIP_PATTERN.format(state_pattern=state_pattern)
        try:
            re.compile(filled_pattern)
        except re.error as e:
            pytest.fail(f"Invalid regex in ADDRESS_CITY_STATE_ZIP_PATTERN: {filled_pattern}\n{e}")

        # Test ADDRESS_STREET_PATTERN
        street_suffixes = "(?:Street|St|Road|Rd)"
        filled_pattern = RegexPatterns.ADDRESS_STREET_PATTERN.format(street_suffixes=street_suffixes)
        try:
            re.compile(filled_pattern)
        except re.error as e:
            pytest.fail(f"Invalid regex in ADDRESS_STREET_PATTERN: {filled_pattern}\n{e}")
