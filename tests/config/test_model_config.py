import pytest
import os
from src.config.model_config import ModelConfig


class TestModelConfig:
    """Tests for the ModelConfig class."""

    def test_project_root_is_string(self):
        """Test that PROJECT_ROOT is a non-empty string."""
        assert isinstance(ModelConfig.PROJECT_ROOT, str)
        assert ModelConfig.PROJECT_ROOT != ""

    def test_intent_model_path_is_string(self):
        """Test that INTENT_MODEL_PATH is a non-empty string."""
        assert isinstance(ModelConfig.INTENT_MODEL_PATH, str)
        assert ModelConfig.INTENT_MODEL_PATH != ""

    def test_ner_model_path_is_string(self):
        """Test that NER_MODEL_PATH is a non-empty string."""
        assert isinstance(ModelConfig.NER_MODEL_PATH, str)
        assert ModelConfig.NER_MODEL_PATH != ""

    def test_spacy_model_name_is_string(self):
        """Test that SPACY_MODEL_NAME is a non-empty string."""
        assert isinstance(ModelConfig.SPACY_MODEL_NAME, str)
        assert ModelConfig.SPACY_MODEL_NAME != ""

    def test_tokenizer_max_length_is_int(self):
        """Test that TOKENIZER_MAX_LENGTH is a positive integer."""
        assert isinstance(ModelConfig.TOKENIZER_MAX_LENGTH, int)
        assert ModelConfig.TOKENIZER_MAX_LENGTH > 0

    def test_spacy_person_label_is_string(self):
        """Test that SPACY_PERSON_LABEL is a non-empty string."""
        assert isinstance(ModelConfig.SPACY_PERSON_LABEL, str)
        assert ModelConfig.SPACY_PERSON_LABEL != ""
