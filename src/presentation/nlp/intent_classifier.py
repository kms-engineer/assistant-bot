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
            model_path = ModelConfig.INTENT_MODEL_PATH

        # Validate model path exists
        if not os.path.exists(model_path):
            raise ValueError(f"Model not found at {model_path}.")

        self.model_path = model_path

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path,
            num_labels=len(IntentConfig.INTENT_LABELS)
        ).to(self.device)

        # Load label mapping
        label_map_path = os.path.join(model_path, "label_map.json")
        with open(label_map_path, 'r') as f:
            label_map = json.load(f)
            self.id2label = {int(k): v for k, v in label_map.items()}

    def predict(self, text: str) -> Tuple[str, float]:
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

    @staticmethod
    def get_intent_labels() -> list:
        return IntentConfig.INTENT_LABELS
