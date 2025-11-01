import pytest
from src.domain.validators.intent_validator import IntentValidator
from src.config import IntentConfig


class TestIntentValidator:
    """Test suite for the IntentValidator."""

    def test_validate_for_intent_success_required_only(self):
        """
        Scenario: All required entities for an intent are present.
        Expected: Validation is successful.
        """
        intent = 'add_contact'  # Requires 'name', 'phone'
        entities = {'name': 'John', 'phone': '12345'}
        result = IntentValidator.validate_for_intent(entities, intent)

        assert result['valid'] is True
        assert result['missing'] == []
        assert result['required'] == IntentConfig.INTENT_REQUIREMENTS[intent]['required']

    def test_validate_for_intent_success_with_optional(self):
        """
        Scenario: All required and some optional entities are present.
        Expected: Validation is successful and optional fields are identified.
        """
        intent = 'add_contact'  # Optional: 'birthday', 'email'
        entities = {'name': 'John', 'phone': '12345', 'email': 'john@test.com'}
        result = IntentValidator.validate_for_intent(entities, intent)

        assert result['valid'] is True
        assert result['missing'] == []
        assert result['has_optional'] is True
        assert result['optional_present'] == ['email']

    def test_validate_for_intent_missing_required(self):
        """
        Scenario: A required entity is missing.
        Expected: Validation fails and identifies the missing entity.
        """
        intent = 'add_contact'
        entities = {'name': 'John'}  # Missing 'phone'
        result = IntentValidator.validate_for_intent(entities, intent)

        assert result['valid'] is False
        assert result['missing'] == ['phone']

    def test_validate_for_intent_empty_required_value(self):
        """
        Scenario: A required entity is present but its value is empty.
        Expected: Validation fails as if the entity was missing.
        """
        intent = 'add_contact'
        entities = {'name': 'John', 'phone': ''}  # Empty phone
        result = IntentValidator.validate_for_intent(entities, intent)

        assert result['valid'] is False
        assert result['missing'] == ['phone']

    def test_validate_for_intent_with_format_error(self):
        """
        Scenario: All entities are present, but a format error flag is set.
        Expected: Validation fails.
        """
        intent = 'add_contact'
        entities = {'name': 'John', 'phone': '123', '_phone_format_error': True}
        result = IntentValidator.validate_for_intent(entities, intent)

        assert result['valid'] is False
        assert result['missing'] == []  # No fields are missing, but format is bad

    def test_validate_for_intent_unknown_intent(self):
        """Scenario: An intent not defined in the config is provided."""
        entities = {'name': 'John'}
        result = IntentValidator.validate_for_intent(entities, 'unknown_intent')

        assert result['valid'] is True  # No required fields, so it's valid
        assert result['missing'] == []
        assert result['required'] == []