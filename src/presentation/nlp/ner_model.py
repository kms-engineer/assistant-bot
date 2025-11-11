from typing import Dict, List, Tuple, Optional, Set
from transformers import AutoModelForTokenClassification, pipeline
from src.config import EntityConfig, ModelConfig
from src.config.intent_requirements import INTENT_REQUIREMENTS
from .base_model import BaseModel


class NERModel(BaseModel):

    LABEL2ID = {label: idx for idx, label in enumerate(EntityConfig.ENTITY_LABELS)}
    ID2LABEL = {idx: label for label, idx in LABEL2ID.items()}

    def __init__(self, model_path: str = None):
        super().__init__(model_path, ModelConfig.NER_MODEL_PATH)

        # Load the pretrained token-classification model without forcing num_labels so
        # the checkpoint's label/head dimensions are preserved. Forcing num_labels
        # can lead to size mismatches when the local EntityConfig differs from the
        # model's training-time label map.
        self.model = AutoModelForTokenClassification.from_pretrained(
            self.model_path
        ).to(self.device)

        self.ner_pipeline = pipeline(
            "token-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple",
            device=self._get_pipeline_device(),
        )

    def extract_entities(
        self, text: str, intent: Optional[str] = None
    ) -> Tuple[Dict[str, Optional[str]], Dict[str, float]]:
        # Get allowed entities for this intent (if provided)
        allowed_entities = self._get_allowed_entities(intent) if intent else None

        # Run NER pipeline
        ner_results = self.ner_pipeline(text)

        # Parse and filter results
        entities, confidences = self._parse_ner_results(
            ner_results, text, allowed_entities
        )
        return entities, confidences

    @staticmethod
    def _get_allowed_entities(intent: str) -> Optional[Set[str]]:
        intent_req = INTENT_REQUIREMENTS.get(intent)
        if not intent_req:
            return None

        allowed = set(intent_req.get("required", []))
        allowed.update(intent_req.get("optional", []))

        return allowed if allowed else None

    @staticmethod
    def _parse_ner_results(
        ner_results: List[Dict], text: str, allowed_entities: Optional[Set[str]] = None
    ) -> Tuple[Dict[str, Optional[str]], Dict[str, float]]:
        entities: Dict[str, Optional[str]] = {
            "name": None,
            "phone": None,
            "email": None,
            "address": None,
            "birthday": None,
            "tag": None,
            "note_text": None,
            "id": None,
            "days": None,
        }

        # Track confidence scores for each entity
        confidences: Dict[str, float] = {}
        entity_scores: Dict[str, List[float]] = (
            {}
        )  # Accumulate scores for multi-token entities
        entity_spans: Dict[str, Dict[str, int]] = (
            {}
        )  # Track start/end positions for accurate extraction

        # Group entities by type
        for result in ner_results:
            entity_group = result["entity_group"]  # e.g., "NAME", "PHONE"
            score = result.get("score", 1.0)  # Confidence score from model
            start = result.get("start", 0)
            end = result.get("end", 0)

            # Map entity group to our entity keys (lowercase)
            entity_key = entity_group.lower()

            # Filter by allowed entities if specified
            if allowed_entities and entity_key not in allowed_entities:
                continue  # Skip entities not allowed for this intent

            # Handle multi-token entities by tracking spans
            if entity_key in entities:
                if entity_key not in entity_spans:
                    # First occurrence of this entity
                    entity_spans[entity_key] = {"start": start, "end": end}
                    entity_scores[entity_key] = [score]
                else:
                    # Extend the span to include this token
                    entity_spans[entity_key]["end"] = end
                    entity_scores[entity_key].append(score)

        # Extract entities using spans from original text
        for key, span in entity_spans.items():
            if span:
                # Extract directly from original text using character positions
                entity_text = text[span["start"] : span["end"]].strip()

                # Clean possessive 's from names
                if key == "name" and entity_text.endswith("'s"):
                    entity_text = entity_text[:-2]

                entities[key] = entity_text
                # Average confidence for multi-token entities
                if key in entity_scores:
                    confidences[key] = sum(entity_scores[key]) / len(entity_scores[key])

        return entities, confidences
