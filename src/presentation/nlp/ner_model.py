import os
import json
from typing import Dict, List, Tuple
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    pipeline
)

class NERModel:

    # IOB2 format labels
    ENTITY_LABELS = [
        "O",              # Outside (not an entity)
        "B-NAME",         # Beginning of name
        "I-NAME",         # Inside name (continuation)
        "B-PHONE",        # Beginning of phone
        "I-PHONE",        # Inside phone
        "B-EMAIL",        # Beginning of email
        "I-EMAIL",        # Inside email
        "B-ADDRESS",      # Beginning of address
        "I-ADDRESS",      # Inside address
        "B-BIRTHDAY",     # Beginning of birthday
        "I-BIRTHDAY",     # Inside birthday
        "B-TAG",          # Beginning of tag
        "I-TAG",          # Inside tag
        "B-NOTE_TEXT",    # Beginning of note text
        "I-NOTE_TEXT",    # Inside note text
        "B-ID",           # Beginning of ID
        "I-ID",           # Inside ID
        "B-DAYS",         # Beginning of days/period
        "I-DAYS",         # Inside days/period
    ]

    # Mapping from label to ID
    LABEL2ID = {label: idx for idx, label in enumerate(ENTITY_LABELS)}
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
            self.model_name = "roberta-base"
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
                num_labels=len(self.ENTITY_LABELS)
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

    def extract_entities(self, text: str, verbose: bool = False) -> Dict[str, str]:
        if not self.is_finetuned:
            # Model not trained, use fallback regex extraction
            if verbose:
                print("[NER] Model not trained, using fallback regex")
            return self._regex_fallback(text)

        if verbose:
            print(f"[NER] Extracting entities from: '{text}'")

        # Use NER pipeline to extract entities
        try:
            ner_results = self.ner_pipeline(text)

            # Parse results into structured format
            entities = self._parse_ner_results(ner_results, text)

            if verbose:
                print(f"[NER] Extracted entities: {entities}")

            return entities

        except Exception as e:
            if verbose:
                print(f"[NER] Error during extraction: {e}")
            # Fallback to regex on error
            return self._regex_fallback(text)

    def _parse_ner_results(self, ner_results: List[Dict], text: str) -> Dict[str, str]:
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

        # Group entities by type
        for result in ner_results:
            entity_group = result['entity_group']  # e.g., "NAME", "PHONE"
            word = result['word'].strip()

            # Clean up RoBERTa tokenization artifacts
            word = word.replace('Ġ', ' ').strip()

            # Map entity group to our entity keys (lowercase)
            entity_key = entity_group.lower()

            # Handle multi-word entities
            if entity_key in entities:
                if entities[entity_key] is None:
                    entities[entity_key] = word
                else:
                    # Append to existing entity
                    if entity_key in ["phone", "email", "birthday", "id"]:
                        # No spaces for structured data
                        entities[entity_key] += word
                    else:
                        # Spaces for text fields
                        entities[entity_key] += " " + word

        # Clean up extracted entities
        for key in entities:
            if entities[key]:
                entities[key] = entities[key].strip()

        return entities

    def _regex_fallback(self, text: str) -> Dict[str, str]:
        import re

        entities = {
            "name": None,
            "phone": None,
            "email": None,
            "address": None,
            "birthday": None
        }

        # Phone pattern
        phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            entities["phone"] = phone_match.group(0)

        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            entities["email"] = email_match.group(0)

        # Birthday pattern (simple)
        birthday_pattern = r'\b\d{1,2}[./]\d{1,2}[./]\d{2,4}\b'
        birthday_match = re.search(birthday_pattern, text)
        if birthday_match:
            entities["birthday"] = birthday_match.group(0)

        # Name extraction (very basic - just capitalized words)
        # Look for 2-3 consecutive capitalized words
        name_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b'
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
