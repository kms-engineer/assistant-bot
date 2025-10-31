import os


class ModelConfig:

    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    INTENT_MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "assistant-bot-intent-classifier")
    """Path to trained intent classifier model."""

    NER_MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "assistant-bot-ner-model")
    """Path to trained NER model."""

    SPACY_MODEL_NAME = "en_core_web_sm"
    """Spacy model name for entity extraction."""

    # Tokenizer settings
    TOKENIZER_MAX_LENGTH = 128
    """Maximum length for tokenizer input."""

    # Spacy entity labels
    SPACY_PERSON_LABEL = "PERSON"
    """Spacy entity label for person names."""
