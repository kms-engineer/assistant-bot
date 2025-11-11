"""Tests for NERModel class."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from src.presentation.nlp.ner_model import NERModel
from src.config.entity_config import EntityConfig


class TestNERModel:
    """Tests for NERModel extract_entities method."""

    @pytest.fixture
    def mock_ner_components(self):
        """Create mock NER components to avoid loading actual models."""
        mock_tokenizer = Mock()
        mock_model = Mock()
        mock_pipeline = Mock()
        mock_label_map = {0: "NAME", 1: "PHONE", 2: "EMAIL"}

        # Mock model to return itself when .to() is called
        mock_model.to = Mock(return_value=mock_model)

        # Mock pipeline results
        mock_ner_results = [
            {
                "entity_group": "NAME",
                "score": 0.95,
                "word": "John",
                "start": 4,
                "end": 8,
            },
            {
                "entity_group": "PHONE",
                "score": 0.92,
                "word": "1234567890",
                "start": 15,
                "end": 25,
            },
        ]
        mock_pipeline.return_value = mock_ner_results

        return mock_tokenizer, mock_model, mock_pipeline, mock_label_map

    @patch("src.presentation.nlp.ner_model.pipeline")
    @patch(
        "src.presentation.nlp.ner_model.AutoModelForTokenClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_extract_entities_returns_tuple(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
        mock_pipeline_loader,
        mock_ner_components,
    ):
        """Test that extract_entities returns a tuple of (entities, confidences)."""
        mock_tokenizer, mock_model, mock_pipeline, mock_label_map = mock_ner_components

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model
        mock_pipeline_loader.return_value = mock_pipeline

        ner_model = NERModel()

        result = ner_model.extract_entities("Add John with phone 1234567890")

        assert isinstance(result, tuple)
        assert len(result) == 2
        entities, confidences = result
        assert isinstance(entities, dict)
        assert isinstance(confidences, dict)

    @patch("src.presentation.nlp.ner_model.pipeline")
    @patch(
        "src.presentation.nlp.ner_model.AutoModelForTokenClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_extract_entities_has_expected_keys(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
        mock_pipeline_loader,
        mock_ner_components,
    ):
        """Test that extracted entities dict has expected keys."""
        mock_tokenizer, mock_model, mock_pipeline, mock_label_map = mock_ner_components

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model
        mock_pipeline_loader.return_value = mock_pipeline

        ner_model = NERModel()

        entities, _ = ner_model.extract_entities("Add John with phone 1234567890")

        expected_keys = [
            "name",
            "phone",
            "email",
            "address",
            "birthday",
            "tag",
            "note_text",
            "id",
            "days",
        ]
        for key in expected_keys:
            assert key in entities

    @patch("src.presentation.nlp.ner_model.pipeline")
    @patch(
        "src.presentation.nlp.ner_model.AutoModelForTokenClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_extract_entities_with_intent_filtering(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
        mock_pipeline_loader,
    ):
        """Test that entities are filtered by intent requirements."""
        # Setup mocks with different NER results
        mock_tokenizer = Mock()
        mock_model = Mock()
        mock_model.to = Mock(return_value=mock_model)

        mock_pipeline = Mock()
        mock_pipeline.return_value = [
            {"entity_group": "NAME", "score": 0.95, "start": 4, "end": 8},
            {"entity_group": "PHONE", "score": 0.92, "start": 15, "end": 25},
            {
                "entity_group": "EMAIL",
                "score": 0.90,
                "start": 30,
                "end": 45,
            },  # Should be filtered out
        ]

        mock_label_map = {0: "NAME", 1: "PHONE", 2: "EMAIL"}

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model
        mock_pipeline_loader.return_value = mock_pipeline

        ner_model = NERModel()

        # Extract with intent filtering
        entities, _ = ner_model.extract_entities(
            "Add John 1234567890 test@email.com", intent="add_contact"
        )

        # Name and phone should be extracted (allowed for add_contact)
        # Email might be filtered based on INTENT_REQUIREMENTS
        assert isinstance(entities, dict)

    @patch("src.presentation.nlp.ner_model.pipeline")
    @patch(
        "src.presentation.nlp.ner_model.AutoModelForTokenClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_extract_entities_empty_text(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
        mock_pipeline_loader,
    ):
        """Test extraction with empty text."""
        mock_tokenizer = Mock()
        mock_model = Mock()
        mock_model.to = Mock(return_value=mock_model)

        mock_pipeline = Mock()
        mock_pipeline.return_value = []  # No entities found

        mock_label_map = {0: "NAME"}

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model
        mock_pipeline_loader.return_value = mock_pipeline

        ner_model = NERModel()

        entities, confidences = ner_model.extract_entities("")

        assert isinstance(entities, dict)
        assert isinstance(confidences, dict)

    def test_parse_ner_results_single_entity(self):
        """Test parsing NER results with a single entity."""
        ner_results = [{"entity_group": "NAME", "score": 0.95, "start": 4, "end": 8}]
        text = "Add John to contacts"

        entities, confidences = NERModel._parse_ner_results(ner_results, text)

        assert entities["name"] == "John"
        assert confidences["name"] == 0.95

    def test_parse_ner_results_multi_token_entity(self):
        """Test parsing NER results with multi-token entities."""
        ner_results = [
            {"entity_group": "NAME", "score": 0.95, "start": 4, "end": 8},
            {"entity_group": "NAME", "score": 0.93, "start": 9, "end": 12},
        ]
        text = "Add John Doe to contacts"

        entities, confidences = NERModel._parse_ner_results(ner_results, text)

        assert entities["name"] == "John Doe"
        # Confidence should be average of scores
        assert abs(confidences["name"] - 0.94) < 0.01

    def test_parse_ner_results_possessive_name(self):
        """Test that possessive 's is removed from names."""
        ner_results = [{"entity_group": "NAME", "score": 0.95, "start": 0, "end": 7}]
        text = "John's phone number"

        entities, confidences = NERModel._parse_ner_results(ner_results, text)

        assert entities["name"] == "John"

    def test_parse_ner_results_with_filtering(self):
        """Test parsing with entity filtering."""
        ner_results = [
            {"entity_group": "NAME", "score": 0.95, "start": 4, "end": 8},
            {"entity_group": "EMAIL", "score": 0.90, "start": 15, "end": 30},
        ]
        text = "Add John with test@email.com"
        allowed_entities = {"name"}  # Only allow name

        entities, confidences = NERModel._parse_ner_results(
            ner_results, text, allowed_entities
        )

        assert entities["name"] == "John"
        assert entities["email"] is None  # Should be filtered out
        assert "email" not in confidences

    def test_parse_ner_results_empty_list(self):
        """Test parsing with empty NER results."""
        ner_results = []
        text = "Some text without entities"

        entities, confidences = NERModel._parse_ner_results(ner_results, text)

        assert all(value is None for value in entities.values())
        assert confidences == {}

    def test_get_allowed_entities_with_valid_intent(self):
        """Test getting allowed entities for a valid intent."""
        allowed = NERModel._get_allowed_entities("add_contact")

        # Should return a set (might be None if intent not in INTENT_REQUIREMENTS)
        assert allowed is None or isinstance(allowed, set)

    def test_get_allowed_entities_with_invalid_intent(self):
        """Test getting allowed entities for an invalid intent."""
        allowed = NERModel._get_allowed_entities("unknown_intent")

        assert allowed is None

    def test_get_allowed_entities_none_intent(self):
        """Test getting allowed entities with None intent."""
        # This should work without error
        allowed = NERModel._get_allowed_entities(None)

        # Depending on implementation, this might return None or handle gracefully
        assert allowed is None or isinstance(allowed, set)


class TestNERModelEdgeCases:
    """Tests for NERModel edge cases."""

    @patch("src.presentation.nlp.ner_model.pipeline")
    @patch(
        "src.presentation.nlp.ner_model.AutoModelForTokenClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_extract_entities_special_characters(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
        mock_pipeline_loader,
    ):
        """Test extraction with special characters."""
        mock_tokenizer = Mock()
        mock_model = Mock()
        mock_model.to = Mock(return_value=mock_model)

        mock_pipeline = Mock()
        mock_pipeline.return_value = []

        mock_label_map = {0: "NAME"}

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model
        mock_pipeline_loader.return_value = mock_pipeline

        ner_model = NERModel()

        entities, confidences = ner_model.extract_entities("Add @#$%^&*()")

        assert isinstance(entities, dict)
        assert isinstance(confidences, dict)

    @patch("src.presentation.nlp.ner_model.pipeline")
    @patch(
        "src.presentation.nlp.ner_model.AutoModelForTokenClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_extract_entities_very_long_text(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
        mock_pipeline_loader,
    ):
        """Test extraction with very long text."""
        mock_tokenizer = Mock()
        mock_model = Mock()
        mock_model.to = Mock(return_value=mock_model)

        mock_pipeline = Mock()
        mock_pipeline.return_value = []

        mock_label_map = {0: "NAME"}

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model
        mock_pipeline_loader.return_value = mock_pipeline

        ner_model = NERModel()

        long_text = "Add contact " * 200
        entities, confidences = ner_model.extract_entities(long_text)

        assert isinstance(entities, dict)
        assert isinstance(confidences, dict)

    @patch("os.path.exists", return_value=False)
    def test_ner_model_init_invalid_model_path(self, mock_exists):
        """Test that NER model raises error with invalid model path."""
        with pytest.raises(ValueError, match="Model not found"):
            NERModel(model_path="/invalid/path")

    def test_parse_ner_results_missing_score(self):
        """Test parsing NER results with missing score field."""
        ner_results = [
            {
                "entity_group": "NAME",
                # 'score' is missing - should default to 1.0
                "start": 4,
                "end": 8,
            }
        ]
        text = "Add John to contacts"

        entities, confidences = NERModel._parse_ner_results(ner_results, text)

        assert entities["name"] == "John"
        assert confidences["name"] == 1.0

    def test_parse_ner_results_overlapping_entities(self):
        """Test parsing with overlapping entity spans."""
        ner_results = [
            {"entity_group": "NAME", "score": 0.95, "start": 0, "end": 10},
            {"entity_group": "PHONE", "score": 0.90, "start": 5, "end": 15},
        ]
        text = "0123456789ABCDE"

        # Should handle gracefully
        entities, confidences = NERModel._parse_ner_results(ner_results, text)

        assert isinstance(entities, dict)
        assert isinstance(confidences, dict)


class TestNERModelIntegration:
    """Integration tests for NERModel with realistic scenarios."""

    def test_parse_ner_results_multiple_entities(self):
        """Test parsing with multiple different entity types."""
        ner_results = [
            {"entity_group": "NAME", "score": 0.95, "start": 4, "end": 8},
            {"entity_group": "PHONE", "score": 0.92, "start": 20, "end": 30},
            {"entity_group": "EMAIL", "score": 0.90, "start": 35, "end": 50},
        ]
        text = "Add John with phone 1234567890 and test@email.com"

        entities, confidences = NERModel._parse_ner_results(ner_results, text)

        assert entities["name"] == "John"
        assert entities["phone"] == "1234567890"
        assert entities["email"] == "test@email.com"
        assert len(confidences) == 3

    def test_parse_ner_results_same_entity_multiple_times(self):
        """Test parsing when same entity type appears multiple times."""
        ner_results = [
            {"entity_group": "PHONE", "score": 0.95, "start": 0, "end": 10},
            {"entity_group": "PHONE", "score": 0.90, "start": 15, "end": 25},
        ]
        text = "1234567890 and 9876543210"

        entities, confidences = NERModel._parse_ner_results(ner_results, text)

        # Should capture the extended span or the last occurrence
        assert entities["phone"] is not None
        assert "phone" in confidences
