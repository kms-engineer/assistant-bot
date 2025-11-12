from abc import ABC, abstractmethod
from typing import Dict
from dataclasses import dataclass, field


@dataclass
class NLPContext:
    user_text: str

    intent: str | None = None
    intent_confidence: float = 0.0
    entities: Dict[str, str] = field(default_factory=dict)
    entity_confidences: Dict[str, float] = field(default_factory=dict)
    validation: Dict = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)
    source: str = "none"


class PipelineStage(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, context: NLPContext) -> NLPContext:
        pass

    def should_skip(self, context: NLPContext) -> bool:
        return False
