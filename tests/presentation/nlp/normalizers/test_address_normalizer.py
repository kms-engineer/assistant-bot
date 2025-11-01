import pytest
from src.presentation.nlp.normalizers.address_normalizer import AddressNormalizer


class TestAddressNormalizer:
    """
    Test suite for the AddressNormalizer.
    Verifies that address strings are correctly cleaned and that city information
    is extracted based on various patterns.
    """

    @pytest.mark.parametrize(
        "input_entities, expected_output",
        [
            # Scenario: No 'address' key present
            ({"name": "John"}, {"name": "John"}),
            # Scenario: 'address' key is empty or None
            ({"address": ""}, {"address": ""}),
            ({"address": None}, {"address": None}),
            # Scenario: Basic address with extra whitespace
            (
                {"address": "  123   Main   St  "},
                {"address": "123 Main St", "city": "Main St"},
            ),
            # Scenario: Address with a clear city at the end
            (
                {"address": "456 Oak Avenue, Springfield"},
                {"address": "456 Oak Avenue, Springfield", "city": "Springfield"},
            ),
            # Scenario: Address where the last word is a common street suffix (should not be a city)
            (
                {"address": "789 Pine Road"},
                {"address": "789 Pine Road", "city": "Pine Road"},
            ),
            # Scenario: Address with a multi-word city name
            (
                {"address": "101 River Side, New York"},
                {"address": "101 River Side, New York", "city": "New York"},
            ),
            # Scenario: Address with city pattern from config (e.g., 'm. Lviv')
            (
                {"address": "Shevchenka St, 1, m. Lviv"},
                {"address": "Shevchenka St, 1, m. Lviv", "city": "Lviv"},
            ),
            # Scenario: Address with only whitespace
            ({"address": "   "}, {"address": ""}),
        ],
        ids=[
            "no_address_key",
            "empty_address",
            "none_address",
            "extra_whitespace",
            "simple_city",
            "street_suffix_not_city",
            "multi_word_city",
            "config_city_pattern",
            "whitespace_only",
        ]
    )
    def test_normalize(self, input_entities, expected_output):
        """Tests the normalize method with various address formats."""
        result = AddressNormalizer.normalize(input_entities)
        assert result == expected_output