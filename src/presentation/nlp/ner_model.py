from typing import Dict, List, Tuple, Optional
from transformers import AutoModelForTokenClassification, pipeline
from src.config import EntityConfig, ModelConfig
from .base_model import BaseModel


class NERModel(BaseModel):

    LABEL2ID = {label: idx for idx, label in enumerate(EntityConfig.ENTITY_LABELS)}
    ID2LABEL = {idx: label for label, idx in LABEL2ID.items()}

    def __init__(self, model_path: str = None):
        super().__init__(model_path, ModelConfig.NER_MODEL_PATH)

        self.model = AutoModelForTokenClassification.from_pretrained(
            self.model_path,
            num_labels=len(EntityConfig.ENTITY_LABELS)
        ).to(self.device)

        self.ner_pipeline = pipeline(
            "token-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple",
            device=self._get_pipeline_device()
        )

    def extract_entities(self, text: str) -> Tuple[Dict[str, Optional[str]], Dict[str, float]]:
        ner_results = self.ner_pipeline(text)
        entities, confidences = self._parse_ner_results(ner_results, text)
        return entities, confidences

    @staticmethod
    def _parse_ner_results(ner_results: List[Dict], text: str) -> Tuple[Dict[str, Optional[str]], Dict[str, float]]:
        entities: Dict[str, Optional[str]] = {
            "name": None,
            "phone": None,
            "email": None,
            "address": None,
            "birthday": None,
            "tag": None,
            "note_text": None,
            "id": None,
            "days": None
        }

        # Track confidence scores for each entity
        confidences: Dict[str, float] = {}
        entity_scores: Dict[str, List[float]] = {}  # Accumulate scores for multi-token entities
        entity_spans: Dict[str, Dict[str, int]] = {}  # Track start/end positions for accurate extraction

        # Group entities by type
        for result in ner_results:
            entity_group = result['entity_group']  # e.g., "NAME", "PHONE"
            score = result.get('score', 1.0)  # Confidence score from model
            start = result.get('start', 0)
            end = result.get('end', 0)

            # Map entity group to our entity keys (lowercase)
            entity_key = entity_group.lower()

            # Handle multi-token entities by tracking spans
            if entity_key in entities:
                if entity_key not in entity_spans:
                    # First occurrence of this entity
                    entity_spans[entity_key] = {'start': start, 'end': end}
                    entity_scores[entity_key] = [score]
                else:
                    # Extend the span to include this token
                    entity_spans[entity_key]['end'] = end
                    entity_scores[entity_key].append(score)

        # Extract entities using spans from original text
        for key, span in entity_spans.items():
            if span:
                # Extract directly from original text using character positions
                entities[key] = text[span['start']:span['end']].strip()
                # Average confidence for multi-token entities
                if key in entity_scores:
                    confidences[key] = sum(entity_scores[key]) / len(entity_scores[key])

        return entities, confidences
