import os
import json
from typing import Tuple
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)
from src.config import IntentConfig, ModelConfig


class IntentClassifier:

    def __init__(self, model_path: str = None, use_pretrained: bool = True):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if model_path and os.path.exists(model_path):
            # Load fine-tuned model
            self.model_name = model_path
            self.is_finetuned = True
        elif use_pretrained:
            # Use base model (RoBERTa shows better performance than DistilBERT)
            self.model_name = ModelConfig.ROBERTA_MODEL_NAME
            self.is_finetuned = False
        else:
            raise ValueError("No model available. Please provide a valid model_path or set use_pretrained=True")

        # Load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        if self.is_finetuned:
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=len(IntentConfig.INTENT_LABELS)
            ).to(self.device)

            # Load label mapping if available
            label_map_path = os.path.join(model_path, "label_map.json")
            if os.path.exists(label_map_path):
                with open(label_map_path, 'r') as f:
                    label_map = json.load(f)
                    self.id2label = {int(k): v for k, v in label_map.items()}
            else:
                self.id2label = {i: label for i, label in enumerate(IntentConfig.INTENT_LABELS)}
        else:
            # Base model - will need to be fine-tuned or use zero-shot
            # For now, create a basic classifier structure
            self.model = None
            self.id2label = {i: label for i, label in enumerate(IntentConfig.INTENT_LABELS)}
            print("WARNING: Using base model without fine-tuning. Classification accuracy will be limited.")

    def predict(self, text: str) -> Tuple[str, float]:
        if not self.is_finetuned:
            # Fallback to simple keyword matching when model not trained
            return self._keyword_fallback(text)

        # Tokenize input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=ModelConfig.TOKENIZER_MAX_LENGTH,
            padding=True
        ).to(self.device)

        # Get predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)

        # Get top prediction
        confidence, pred_idx = torch.max(probs, dim=-1)
        intent_label = self.id2label[pred_idx.item()]
        confidence_score = confidence.item()

        return intent_label, confidence_score

    def _keyword_fallback(self, text: str) -> Tuple[str, float]:
        text_lower = text.lower()

        # Get keyword map from config
        keyword_map = IntentConfig.KEYWORD_MAP

        # Score each intent
        scores = {}
        for intent, keywords in keyword_map.items():
            max_score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    # Higher score for longer matches
                    score = len(keyword) / len(text_lower)
                    # Boost if keyword is at start
                    if text_lower.startswith(keyword):
                        score *= 1.5
                    # Extra boost for exact matches
                    if keyword == text_lower:
                        score *= 2.0
                    max_score = max(max_score, score)

            if max_score > 0:
                scores[intent] = max_score

        # Special handling for conflicting patterns
        # If both "show all" patterns match, prefer specific one
        if "show_notes" in scores and "list_all_contacts" in scores:
            if "notes" in text_lower or "note" in text_lower:
                # It's about notes
                scores["show_notes"] *= 2.0
            elif "contact" in text_lower or "everyone" in text_lower:
                # It's about contacts
                scores["list_all_contacts"] *= 2.0

        # Return best match
        if scores:
            best_intent = max(scores.items(), key=lambda x: x[1])
            # Normalize confidence to keyword confidence range
            confidence = min(
                IntentConfig.KEYWORD_CONFIDENCE_MAX,
                IntentConfig.KEYWORD_CONFIDENCE_MIN + best_intent[1]
            )
            return best_intent[0], confidence

        # Unknown intent
        return IntentConfig.DEFAULT_INTENT, IntentConfig.DEFAULT_INTENT_CONFIDENCE

    def get_intent_labels(self) -> list:
        return IntentConfig.INTENT_LABELS
