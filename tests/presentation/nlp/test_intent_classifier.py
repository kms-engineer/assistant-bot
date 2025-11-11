"""Tests for IntentClassifier class."""

import pytest
import torch
from unittest.mock import Mock, MagicMock, patch
from src.presentation.nlp.intent_classifier import IntentClassifier
from src.config.intent_config import IntentConfig


class TestIntentClassifier:
    """Tests for IntentClassifier predict method."""

    @pytest.fixture
    def mock_model_components(self):
        """Create mock model components to avoid loading actual models."""
        mock_tokenizer = Mock()
        mock_model = Mock()
        mock_label_map = {0: "add_contact", 1: "search_contacts", 2: "add_note"}

        # Mock tokenizer to return proper tensors
        mock_inputs = {
            "input_ids": torch.tensor([[1, 2, 3]]),
            "attention_mask": torch.tensor([[1, 1, 1]]),
        }
        mock_tokenizer.return_value = MagicMock()
        mock_tokenizer.return_value.to = Mock(return_value=mock_inputs)

        # Mock model to return itself when .to() is called
        mock_model.to = Mock(return_value=mock_model)

        # Mock model outputs with actual torch tensors
        mock_outputs = Mock()
        mock_outputs.logits = torch.tensor(
            [[2.0, 1.0, 0.5]]
        )  # Highest score for index 0
        mock_model.return_value = mock_outputs

        return mock_tokenizer, mock_model, mock_label_map

    @patch(
        "src.presentation.nlp.intent_classifier.AutoModelForSequenceClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_predict_returns_tuple(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
        mock_model_components,
    ):
        """Test that predict returns a tuple of (intent, confidence)."""
        mock_tokenizer, mock_model, mock_label_map = mock_model_components

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model

        classifier = IntentClassifier()

        result = classifier.predict("Add John to contacts")

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)  # Intent label
        assert isinstance(result[1], float)  # Confidence score

    @patch(
        "src.presentation.nlp.intent_classifier.AutoModelForSequenceClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_predict_confidence_range(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
        mock_model_components,
    ):
        """Test that confidence score is between 0 and 1."""
        mock_tokenizer, mock_model, mock_label_map = mock_model_components

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model

        classifier = IntentClassifier()

        _, confidence = classifier.predict("Search for Alice")

        assert 0.0 <= confidence <= 1.0

    @patch(
        "src.presentation.nlp.intent_classifier.AutoModelForSequenceClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_predict_empty_text(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
        mock_model_components,
    ):
        """Test prediction with empty text."""
        mock_tokenizer, mock_model, mock_label_map = mock_model_components

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model

        classifier = IntentClassifier()

        intent, confidence = classifier.predict("")

        assert isinstance(intent, str)
        assert isinstance(confidence, float)

    @patch(
        "src.presentation.nlp.intent_classifier.AutoModelForSequenceClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_predict_long_text(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
        mock_model_components,
    ):
        """Test prediction with very long text."""
        mock_tokenizer, mock_model, mock_label_map = mock_model_components

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model

        classifier = IntentClassifier()

        long_text = "Add contact " * 200  # Very long input
        intent, confidence = classifier.predict(long_text)

        assert isinstance(intent, str)
        assert isinstance(confidence, float)

    def test_get_intent_labels_returns_list(self):
        """Test that get_intent_labels returns a list."""
        labels = IntentClassifier.get_intent_labels()

        assert isinstance(labels, list)
        assert len(labels) > 0

    def test_get_intent_labels_contains_expected_intents(self):
        """Test that get_intent_labels contains expected intents."""
        labels = IntentClassifier.get_intent_labels()

        # Should contain some expected intents
        expected_intents = ["add_contact", "search_contacts", "add_note"]

        # At least one should be present
        assert any(intent in labels for intent in expected_intents)


class TestIntentClassifierEdgeCases:
    """Tests for IntentClassifier edge cases."""

    @patch(
        "src.presentation.nlp.intent_classifier.AutoModelForSequenceClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_predict_special_characters(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
    ):
        """Test prediction with special characters."""
        # Setup mocks
        mock_tokenizer = Mock()
        mock_model = Mock()
        mock_label_map = {0: "add_contact"}

        mock_inputs = {
            "input_ids": torch.tensor([[1, 2, 3]]),
            "attention_mask": torch.tensor([[1, 1, 1]]),
        }
        mock_tokenizer.return_value = MagicMock()
        mock_tokenizer.return_value.to = Mock(return_value=mock_inputs)

        # Mock model to return itself when .to() is called
        mock_model.to = Mock(return_value=mock_model)

        mock_outputs = Mock()
        mock_outputs.logits = torch.tensor([[1.0]])
        mock_model.return_value = mock_outputs

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model

        classifier = IntentClassifier()

        special_text = "Add @#$%^&*() contact"
        intent, confidence = classifier.predict(special_text)

        assert isinstance(intent, str)
        assert isinstance(confidence, float)

    @patch(
        "src.presentation.nlp.intent_classifier.AutoModelForSequenceClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_predict_numbers_only(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
    ):
        """Test prediction with numbers only."""
        # Setup mocks
        mock_tokenizer = Mock()
        mock_model = Mock()
        mock_label_map = {0: "unknown"}

        mock_inputs = {
            "input_ids": torch.tensor([[1, 2, 3]]),
            "attention_mask": torch.tensor([[1, 1, 1]]),
        }
        mock_tokenizer.return_value = MagicMock()
        mock_tokenizer.return_value.to = Mock(return_value=mock_inputs)

        # Mock model to return itself when .to() is called
        mock_model.to = Mock(return_value=mock_model)

        mock_outputs = Mock()
        mock_outputs.logits = torch.tensor([[0.5]])
        mock_model.return_value = mock_outputs

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model

        classifier = IntentClassifier()

        numbers_text = "1234567890"
        intent, confidence = classifier.predict(numbers_text)

        assert isinstance(intent, str)
        assert isinstance(confidence, float)

    @patch("os.path.exists", return_value=False)
    def test_classifier_init_invalid_model_path(self, mock_exists):
        """Test that classifier raises error with invalid model path."""
        with pytest.raises(ValueError, match="Model not found"):
            IntentClassifier(model_path="/invalid/path")


class TestIntentClassifierIntegration:
    """Integration tests for IntentClassifier with real-like scenarios."""

    @patch(
        "src.presentation.nlp.intent_classifier.AutoModelForSequenceClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_multiple_predictions(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
    ):
        """Test making multiple predictions in sequence."""
        # Setup mocks
        mock_tokenizer = Mock()
        mock_model = Mock()
        mock_label_map = {0: "add_contact", 1: "search_contacts", 2: "add_note"}

        mock_inputs = {
            "input_ids": torch.tensor([[1, 2, 3]]),
            "attention_mask": torch.tensor([[1, 1, 1]]),
        }
        mock_tokenizer.return_value = MagicMock()
        mock_tokenizer.return_value.to = Mock(return_value=mock_inputs)

        # Mock model to return itself when .to() is called
        mock_model.to = Mock(return_value=mock_model)

        # Different outputs for different predictions
        mock_outputs_1 = Mock()
        mock_outputs_1.logits = torch.tensor([[2.0, 1.0, 0.5]])

        mock_outputs_2 = Mock()
        mock_outputs_2.logits = torch.tensor([[0.5, 2.0, 1.0]])

        mock_model.side_effect = [mock_outputs_1, mock_outputs_2]

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model

        classifier = IntentClassifier()

        # Make multiple predictions
        intent1, conf1 = classifier.predict("Add John")
        intent2, conf2 = classifier.predict("Search Alice")

        # Both should return valid results
        assert isinstance(intent1, str)
        assert isinstance(intent2, str)
        assert 0.0 <= conf1 <= 1.0
        assert 0.0 <= conf2 <= 1.0

    @patch(
        "src.presentation.nlp.intent_classifier.AutoModelForSequenceClassification.from_pretrained"
    )
    @patch("src.presentation.nlp.base_model.AutoTokenizer.from_pretrained")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.load")
    def test_predict_various_intents(
        self,
        mock_json_load,
        mock_open,
        mock_exists,
        mock_tokenizer_loader,
        mock_model_loader,
    ):
        """Test prediction with various intent types."""
        # Setup mocks
        mock_tokenizer = Mock()
        mock_model = Mock()
        mock_label_map = {
            0: "add_contact",
            1: "edit_phone",
            2: "delete_contact",
            3: "search_contacts",
            4: "add_note",
        }

        mock_inputs = {
            "input_ids": torch.tensor([[1, 2, 3]]),
            "attention_mask": torch.tensor([[1, 1, 1]]),
        }
        mock_tokenizer.return_value = MagicMock()
        mock_tokenizer.return_value.to = Mock(return_value=mock_inputs)

        # Mock model to return itself when .to() is called
        mock_model.to = Mock(return_value=mock_model)

        mock_outputs = Mock()
        mock_outputs.logits = torch.tensor([[1.0, 0.5, 0.3, 0.2, 0.1]])
        mock_model.return_value = mock_outputs

        mock_json_load.return_value = mock_label_map
        mock_tokenizer_loader.return_value = mock_tokenizer
        mock_model_loader.return_value = mock_model

        classifier = IntentClassifier()

        test_inputs = [
            "Add new contact John",
            "Edit phone number",
            "Delete contact Alice",
            "Search for Bob",
            "Add note about meeting",
        ]

        for text in test_inputs:
            intent, confidence = classifier.predict(text)
            assert isinstance(intent, str)
            assert isinstance(confidence, float)
            assert intent in mock_label_map.values()
