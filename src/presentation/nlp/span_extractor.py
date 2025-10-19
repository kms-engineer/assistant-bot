from typing import Dict, List, Tuple

from .extractors import (
    Entity,
    LibraryExtractor,
    RegexExtractor,
    HeuristicExtractor
)


class SpanExtractor:

    def __init__(self, model_path: str = None, use_pretrained: bool = True, verbose: bool = False):
        self.verbose = verbose
        self.regex_extractor = RegexExtractor()

        # Log available libraries
        if self.verbose:
            print("\n[SpanExtractor] Initializing multi-strategy extraction...")
            libraries = LibraryExtractor.get_available_libraries()
            for lib_name, available in libraries.items():
                print(f"  - {lib_name}: {'✓' if available else '✗'}")

    def extract(self, text: str) -> Tuple[Dict[str, str], List[Dict], Dict[str, float]]:
        if self.verbose:
            print(f"\n[SpanExtractor] Extracting from: '{text}'")

        # Extract all entities using multi-strategy approach
        all_entities = []

        # Strategy 1: Library-based extraction (highest confidence)
        all_entities.extend(LibraryExtractor.extract_all(text))

        # Strategy 2: Regex-based extraction
        all_entities.extend(self.regex_extractor.extract_all(text))

        # Strategy 3: Heuristic-based extraction (for names and addresses)
        all_entities.extend(HeuristicExtractor.extract_all(text))

        # Resolve conflicts: prefer higher confidence entities
        resolved_entities = self._resolve_conflicts(all_entities)

        # Convert to output format
        entities = {}
        raw_spans = []
        probabilities = {}

        for entity in resolved_entities:
            entities[entity.entity_type] = entity.text
            probabilities[entity.entity_type] = entity.confidence
            raw_spans.append({
                'type': entity.entity_type,
                'text': entity.text,
                'start': entity.start,
                'end': entity.end,
                'confidence': entity.confidence,
                'strategy': entity.strategy.value
            })

        if self.verbose:
            print(f"[SpanExtractor] Extracted {len(entities)} entities: {list(entities.keys())}")
            for entity_type, entity_value in entities.items():
                strategy = next((e.strategy.value for e in resolved_entities if e.entity_type == entity_type), 'unknown')
                conf = probabilities.get(entity_type, 0.0)
                print(f"  - {entity_type}: '{entity_value}' (confidence: {conf:.2f}, strategy: {strategy})")

        return entities, raw_spans, probabilities

    def _resolve_conflicts(self, entities: List[Entity]) -> List[Entity]:
        if not entities:
            return []

        # Sort by confidence (descending)
        sorted_entities = sorted(entities, key=lambda e: e.confidence, reverse=True)

        # Keep track of used spans
        resolved = []
        used_spans = []

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
