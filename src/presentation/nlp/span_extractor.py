from typing import Dict, List, Tuple, Optional, Set

from .extractors import Entity, LibraryExtractor, RegexExtractor, HeuristicExtractor
from src.config.intent_requirements import INTENT_REQUIREMENTS


class SpanExtractor:

    def __init__(self):
        self.regex_extractor = RegexExtractor()

    def extract(
        self, text: str, intent: Optional[str] = None
    ) -> Tuple[Dict[str, str], List[Dict], Dict[str, float]]:
        # Get allowed entities for this intent
        allowed_entities = self._get_allowed_entities(intent) if intent else None

        # Run all extractors
        all_entities = []
        all_entities.extend(LibraryExtractor.extract_all(text))
        all_entities.extend(self.regex_extractor.extract_all(text))
        all_entities.extend(HeuristicExtractor.extract_all(text))

        # Filter by allowed entities if intent provided
        if allowed_entities:
            all_entities = [
                e for e in all_entities if e.entity_type in allowed_entities
            ]

        resolved_entities = self._resolve_conflicts(all_entities)

        entities = {}
        raw_spans = []
        probabilities = {}

        for entity in resolved_entities:
            entities[entity.entity_type] = entity.text
            probabilities[entity.entity_type] = entity.confidence
            raw_spans.append(
                {
                    "type": entity.entity_type,
                    "text": entity.text,
                    "start": entity.start,
                    "end": entity.end,
                    "confidence": entity.confidence,
                    "strategy": entity.strategy.value,
                }
            )

        return entities, raw_spans, probabilities

    @staticmethod
    def _get_allowed_entities(intent: str) -> Optional[Set[str]]:
        intent_req = INTENT_REQUIREMENTS.get(intent)
        if not intent_req:
            return None

        allowed = set(intent_req.get("required", []))
        allowed.update(intent_req.get("optional", []))

        return allowed if allowed else None

    @staticmethod
    def _resolve_conflicts(entities: List[Entity]) -> List[Entity]:
        if not entities:
            return []

        # Sort by confidence (descending)
        sorted_entities = sorted(entities, key=lambda e: e.confidence, reverse=True)

        # Keep track of used spans
        resolved = []
        used_spans: list[Tuple[int, int]] = []

        for entity in sorted_entities:
            # Check if this entity overlaps with any already selected
            overlaps = False
            for used_start, used_end in used_spans:
                if not (entity.end <= used_start or entity.start >= used_end):
                    overlaps = True
                    break

            if not overlaps:
                resolved.append(entity)
                used_spans.append((entity.start, entity.end))

        # Sort by start position for final output
        resolved.sort(key=lambda e: e.start)
        return resolved
