import pytest
from unittest.mock import Mock, patch
from src.domain.utils.id_generator import IDGenerator


class TestIDGenerator:
    """Tests for the IDGenerator class."""

    def test_generate_id_returns_string(self):
        """Test that generate_id returns a string."""
        new_id = IDGenerator.generate_id()
        assert isinstance(new_id, str)

    def test_generate_id_returns_unique_values(self):
        """Test that generate_id returns unique IDs on subsequent calls."""
        id1 = IDGenerator.generate_id()
        id2 = IDGenerator.generate_id()
        assert id1 != id2

    def test_generate_unique_id_success_first_try(self):
        """Test generate_unique_id when the first generated ID is unique."""
        existing_ids_provider = Mock(return_value={"id1", "id2"})
        with patch(
            "src.domain.utils.id_generator.uuid.uuid4", return_value="new-unique-id"
        ):
            new_id = IDGenerator.generate_unique_id(existing_ids_provider)
            assert new_id == "new-unique-id"
            existing_ids_provider.assert_called_once()

    def test_generate_unique_id_success_after_few_tries(self):
        """Test generate_unique_id when it takes a few attempts to find a unique ID."""
        existing_ids = {"id1", "id2"}
        generated_ids = ["id1", "id2", "new-unique-id"]

        provider_mock = Mock(return_value=existing_ids)

        with patch(
            "src.domain.utils.id_generator.uuid.uuid4", side_effect=generated_ids
        ) as mock_uuid4:
            new_id = IDGenerator.generate_unique_id(provider_mock)
            assert new_id == "new-unique-id"
            assert provider_mock.call_count == 3
            assert mock_uuid4.call_count == 3

    def test_generate_unique_id_raises_runtime_error(self):
        """Test that generate_unique_id raises RuntimeError after max attempts."""
        existing_ids = {"id1", "id2"}
        generated_ids = ["id1"] * 100

        provider_mock = Mock(return_value=existing_ids)

        with patch(
            "src.domain.utils.id_generator.uuid.uuid4", side_effect=generated_ids
        ) as mock_uuid4:
            with pytest.raises(
                RuntimeError,
                match="Unable to generate unique ID after maximum attempts",
            ):
                IDGenerator.generate_unique_id(provider_mock)
            assert provider_mock.call_count == 100
            assert mock_uuid4.call_count == 100
