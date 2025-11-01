import pytest
from unittest.mock import patch
from src.domain.validators.base_validator import BaseValidator


class ConcreteValidator(BaseValidator):
    """A concrete implementation of BaseValidator for testing purposes."""
    @staticmethod
    def validate(value: str):
        # This method will be mocked in tests
        pass


class TestBaseValidator:
    """Test suite for the abstract BaseValidator class."""

    def test_validate_and_raise_success(self):
        """
        Scenario: validate() returns True.
        Expected: validate_and_raise() should not raise an exception.
        """
        with patch.object(ConcreteValidator, 'validate', return_value=True):
            ConcreteValidator.validate_and_raise("valid_value")  # Should not raise

    def test_validate_and_raise_failure(self):
        """
        Scenario: validate() returns an error message string.
        Expected: validate_and_raise() should raise a ValueError with the same message.
        """
        error_message = "This is an error"
        with patch.object(ConcreteValidator, 'validate', return_value=error_message):
            with pytest.raises(ValueError, match=error_message):
                ConcreteValidator.validate_and_raise("invalid_value")