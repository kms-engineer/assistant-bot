import os
import json
from typing import Dict
import torch
from transformers import AutoTokenizer


class BaseModel:

    def __init__(self, model_path: str, default_path: str):
        self.device = self._select_device()
        print(f"Using device: {self.device}")

        self.model_path = model_path or default_path
        self._validate_model_path()

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.id2label = self._load_label_map()

    @staticmethod
    def _select_device() -> str:
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def _validate_model_path(self) -> None:
        if not os.path.exists(self.model_path):
            raise ValueError(f"Model not found at {self.model_path}.")

    def _load_label_map(self) -> Dict[int, str]:
        label_map_path = os.path.join(self.model_path, "label_map.json")
        with open(label_map_path, 'r') as f:
            label_map = json.load(f)
            return {int(k): v for k, v in label_map.items()}

    def _get_pipeline_device(self):
        if self.device == "cuda":
            return 0
        elif self.device == "mps":
            return torch.device("mps")
        return -1
