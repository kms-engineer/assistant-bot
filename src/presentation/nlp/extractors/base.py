from dataclasses import dataclass
from enum import Enum
from src.config import EntityConfig


class ExtractionStrategy(Enum):
    LIBRARY = "library"
    REGEX = "regex"
    ML = "ml"
    HEURISTIC = "heuristic"


@dataclass
class Entity:
    text: str
    start: int
    end: int
    entity_type: str
    confidence: float = 1.0
    strategy: ExtractionStrategy = ExtractionStrategy.REGEX


def is_stop_word(word: str) -> bool:
    return word in EntityConfig.HEURISTIC_STOP_WORDS
