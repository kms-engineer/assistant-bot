import pytest
from unittest.mock import patch
from src.presentation.nlp.normalizers.birthday_normalizer import BirthdayNormalizer


class TestBirthdayNormalizer:
    """
    Test suite for the BirthdayNormalizer.
    Verifies parsing of various date formats, age calculation, and graceful
    fallback when the optional 'dateutil' library is unavailable.
    """

    @pytest.mark.parametrize(
        "input_entities, expected_birthday, dateutil_available",
        [
            # Scenario: With dateutil, standard format
            ({"birthday": "01.01.2000"}, "01.01.2000", True),
            # Scenario: With dateutil, fuzzy format
            ({"birthday": "Jan 1st, 2000"}, "01.01.2000", True),
            # Scenario: Without dateutil, supported manual format (DD.MM.YYYY)
            ({"birthday": "25.12.1995"}, "25.12.1995", False),
            # Scenario: Without dateutil, supported manual format (YYYY-MM-DD)
            ({"birthday": "1995-12-25"}, "25.12.1995", False),
        ],
        ids=[
            "dateutil_standard",
            "dateutil_fuzzy",
            "no_dateutil_dd_mm_yyyy",
            "no_dateutil_yyyy_mm_dd",
        ]
    )
    def test_normalize_valid_date(self, input_entities, expected_birthday, dateutil_available):
        """Tests normalization of valid birthday strings."""
        with patch('src.presentation.nlp.normalizers.birthday_normalizer.DATEUTIL_AVAILABLE', dateutil_available):
            result = BirthdayNormalizer.normalize(input_entities.copy())

            assert result['_birthday_valid'] is True
            assert result['birthday'] == expected_birthday
            assert 'age' in result
            assert isinstance(result['age'], int)

    @pytest.mark.parametrize(
        "input_entities, dateutil_available",
        [
            # Scenario: With dateutil, invalid string
            ({"birthday": "not a real date"}, True),
            # Scenario: Without dateutil, unsupported format
            ({"birthday": "Jan 1st, 2000"}, False),
            # Scenario: Gibberish input
            ({"birthday": "xyz"}, False),
        ],
        ids=[
            "dateutil_invalid",
            "no_dateutil_unsupported",
            "gibberish_input",
        ]
    )
    def test_normalize_invalid_date(self, input_entities, dateutil_available):
        """Tests handling of invalid or unparseable birthday strings."""
        with patch('src.presentation.nlp.normalizers.birthday_normalizer.DATEUTIL_AVAILABLE', dateutil_available):
            result = BirthdayNormalizer.normalize(input_entities.copy())

            assert result['_birthday_valid'] is False
            assert '_validation_errors' in result
            assert any(f"Failed to parse birthday: {input_entities['birthday']}" in e for e in result['_validation_errors'])

    @pytest.mark.parametrize(
        "input_entities",
        [
            # Scenario: No 'birthday' key
            ({"name": "John"}),
            # Scenario: 'birthday' key is empty or None
            ({"birthday": ""}),
            ({"birthday": None}),
        ],
        ids=[
            "no_birthday_key",
            "empty_birthday",
            "none_birthday",
        ]
    )
    def test_normalize_no_input(self, input_entities):
        """Tests that the normalizer does nothing if the birthday field is missing or empty."""
        original_entities = input_entities.copy()
        result = BirthdayNormalizer.normalize(input_entities)
        assert result == original_entities

    def test_calculate_age(self):
        """
        Tests the internal _calculate_age helper method.
        This test is independent of the normalization logic.
        """
        from datetime import datetime, timedelta

        # A person who just turned 20
        twenty_years_ago = datetime.now() - timedelta(days=365.25 * 20)
        assert BirthdayNormalizer._calculate_age(twenty_years_ago) == 20

        # A person who will turn 20 tomorrow
        almost_twenty = datetime.now() - timedelta(days=365.25 * 20) + timedelta(days=1)
        assert BirthdayNormalizer._calculate_age(almost_twenty) == 19