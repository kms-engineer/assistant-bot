import os
import json
from typing import Dict, List, Tuple
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

    def __init__(self, model_path: str = None, use_pretrained: bool = True):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if model_path and os.path.exists(model_path):
            # Load fine-tuned model
            self.model_name = model_path
            self.is_finetuned = True
            print(f"Loading fine-tuned NER model from {model_path}")
        elif use_pretrained:
            # Use base model (will need fine-tuning for production)
            self.model_name = ModelConfig.ROBERTA_MODEL_NAME
            self.is_finetuned = False
            print("WARNING: Using base RoBERTa model without NER fine-tuning.")
            print("NER accuracy will be limited until model is trained.")
            print("Run scripts/train_ner_model.py to train the model.")
        else:
            raise ValueError("No model available. Please provide a valid model_path or set use_pretrained=True")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        if self.is_finetuned:
            # Load fine-tuned token classification model
            self.model = AutoModelForTokenClassification.from_pretrained(
                self.model_name,
                num_labels=len(EntityConfig.ENTITY_LABELS)
            ).to(self.device)

            # Load label mapping if available
            label_map_path = os.path.join(model_path, "label_map.json")
            if os.path.exists(label_map_path):
                with open(label_map_path, 'r') as f:
                    label_map = json.load(f)
                    self.id2label = {int(k): v for k, v in label_map.items()}
            else:
                self.id2label = self.ID2LABEL

            # Create NER pipeline for easier inference
            self.ner_pipeline = pipeline(
                "token-classification",
                model=self.model,
                tokenizer=self.tokenizer,
                aggregation_strategy="simple",  # Merge B-/I- tokens
                device=0 if self.device == "cuda" else -1
            )
        else:
            # Base model not trained for NER - will use fallback regex
            self.model = None
            self.ner_pipeline = None
            self.id2label = self.ID2LABEL

    def extract_entities(self, text: str, verbose: bool = False) -> Tuple[Dict[str, str], Dict[str, float]]:
        if not self.is_finetuned:
            # Model not trained, use fallback regex extraction
            if verbose:
                print("[NER] Model not trained, using fallback regex")
            return self._regex_fallback(text), {}

        if verbose:
            print(f"[NER] Extracting entities from: '{text}'")

        # Use NER pipeline to extract entities
        try:
            ner_results = self.ner_pipeline(text)

            # Parse results into structured format with confidence scores
            entities, confidences = self._parse_ner_results(ner_results, text)

            if verbose:
                print(f"[NER] Extracted entities: {entities}")
                print(f"[NER] Confidence scores: {confidences}")

            return entities, confidences

        except Exception as e:
            if verbose:
                print(f"[NER] Error during extraction: {e}")
            # Fallback to regex on error
            return self._regex_fallback(text), {}

    def _parse_ner_results(self, ner_results: List[Dict], text: str) -> Tuple[Dict[str, str], Dict[str, float]]:
        entities = {
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
        confidences = {}
        entity_scores = {}  # Accumulate scores for multi-token entities
        entity_spans = {}  # Track start/end positions for accurate extraction

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

    def _regex_fallback(self, text: str) -> Dict[str, str]:
        import re
        from src.config import RegexPatterns

        entities = {
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

        # UUID pattern (for note IDs)
        uuid_pattern = RegexPatterns.UUID_PATTERN
        uuid_match = re.search(uuid_pattern, text)
        if uuid_match:
            entities["id"] = uuid_match.group(0)

        # Phone pattern
        phone_pattern = RegexPatterns.PHONE_PATTERN
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            entities["phone"] = phone_match.group(0)

        # Email pattern
        email_pattern = RegexPatterns.EMAIL_PATTERN
        email_match = re.search(email_pattern, text)
        if email_match:
            entities["email"] = email_match.group(0)

        # Birthday pattern (simple)
        birthday_pattern = RegexPatterns.BIRTHDAY_PATTERN
        birthday_match = re.search(birthday_pattern, text)
        if birthday_match:
            entities["birthday"] = birthday_match.group(0)

        # Tag pattern
        tag_pattern = RegexPatterns.TAG_PATTERN
        tag_match = re.search(tag_pattern, text)
        if tag_match:
            entities["tag"] = tag_match.group(0)

        # Days pattern (for birthday lists)
        days_pattern = r'\b(\d+)\s*days?\b'
        days_match = re.search(days_pattern, text, re.IGNORECASE)
        if days_match:
            entities["days"] = days_match.group(1)

        # Name extraction (very basic - just capitalized words)
        # Look for 2-3 consecutive capitalized words
        name_pattern = RegexPatterns.NAME_FULL_PATTERN
        name_match = re.search(name_pattern, text)
        if name_match:
            entities["name"] = name_match.group(0)

        return entities

    def predict_tokens(self, text: str) -> Tuple[List[str], List[str]]:
        if not self.is_finetuned:
            raise ValueError("Model not trained. Cannot predict token labels.")

        # Tokenize
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=128,
            padding=True,
            return_offsets_mapping=True
        ).to(self.device)

        # Get predictions
        with torch.no_grad():
            outputs = self.model(**{k: v for k, v in inputs.items() if k != 'offset_mapping'})
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=-1)

        # Convert to labels
        tokens = self.tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
        labels = [self.id2label[pred.item()] for pred in predictions[0]]

        return tokens, labels

    def get_entity_labels(self) -> List[str]:
        return self.ENTITY_LABELS
