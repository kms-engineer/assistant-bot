import os
import json
from typing import Dict, List, Tuple, Optional
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    pipeline
)
from src.config import EntityConfig, ModelConfig

class NERModel:

    # Mapping from label to ID (generated from config)
    LABEL2ID = {label: idx for idx, label in enumerate(EntityConfig.ENTITY_LABELS)}
    ID2LABEL = {idx: label for label, idx in LABEL2ID.items()}

    def __init__(self, model_path: str = None):
        # Select best available device: CUDA (NVIDIA) > MPS (Apple Silicon) > CPU
        if torch.cuda.is_available():
            self.device = "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            self.device = "mps"
        else:
            self.device = "cpu"

        print(f"Using device: {self.device}")

        # Use default path if not provided
        if model_path is None:
            model_path = ModelConfig.NER_MODEL_PATH

        # Validate model path exists
        if not os.path.exists(model_path):
            raise ValueError(f"Model not found at {model_path}.")

        self.model_path = model_path
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForTokenClassification.from_pretrained(
            model_path,
            num_labels=len(EntityConfig.ENTITY_LABELS)
        ).to(self.device)

        # Load label mapping
        label_map_path = os.path.join(model_path, "label_map.json")
        with open(label_map_path, 'r') as f:
            label_map = json.load(f)
            self.id2label = {int(k): v for k, v in label_map.items()}

        # Create NER pipeline for easier inference
        # Note: pipeline device parameter: 0 for cuda, -1 for cpu, or torch.device for mps
        if self.device == "cuda":
            pipeline_device = 0
        elif self.device == "mps":
            pipeline_device = torch.device("mps")
        else:
            pipeline_device = -1

        self.ner_pipeline = pipeline(
            "token-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple",  # Merge B-/I- tokens
            device=pipeline_device
        )

    def extract_entities(self, text: str, verbose: bool = False) -> Tuple[Dict[str, Optional[str]], Dict[str, float]]:
        # Use NER pipeline to extract entities
        ner_results = self.ner_pipeline(text)

        # Parse results into structured format with confidence scores
        entities, confidences = self._parse_ner_results(ner_results, text)

        if verbose:
            print(f"[NER] Extracted entities: {entities}")
            print(f"[NER] Confidence scores: {confidences}")

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
