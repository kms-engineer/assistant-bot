from typing import Tuple
import torch
from transformers import AutoModelForSequenceClassification
from src.config import IntentConfig, ModelConfig
from .base_model import BaseModel


class IntentClassifier(BaseModel):

    def __init__(self, model_path: str = None):
        super().__init__(model_path, ModelConfig.INTENT_MODEL_PATH)

        # Load model - num_labels is automatically loaded from model config
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_path
        ).to(self.device)

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
