
class ModelConfig:

    # NLP model names
    ROBERTA_MODEL_NAME = "roberta-base"
    """Model name for RoBERTa-based models (intent classifier and NER)."""

    SPACY_MODEL_NAME = "en_core_web_sm"
    """Spacy model name for entity extraction."""

    # Tokenizer settings
    TOKENIZER_MAX_LENGTH = 128
    """Maximum length for tokenizer input."""

    # Spacy entity labels
    SPACY_PERSON_LABEL = "PERSON"
    """Spacy entity label for person names."""
