from typing import Optional, Tuple
from src.config.nlp_config import NLPConfig


class KeywordIntentMatcher:

    def __init__(self):
        # Precompile patterns for faster matching
        self._compiled_patterns = {}
        for intent, patterns in NLPConfig.INTENT_PATTERNS.items():
            self._compiled_patterns[intent] = [
                self._compile_pattern(p) for p in patterns
            ]

    @staticmethod
    def _compile_pattern(pattern: dict) -> dict:
        return {
            "required": [[kw.lower() for kw in group] for group in pattern["required"]],
            "optional": [kw.lower() for kw in pattern["optional"]],
            "confidence": pattern["confidence"]
        }

    @staticmethod
    def _matches_pattern(text_lower: str, pattern: dict) -> Tuple[bool, float]:
        # Check required keyword groups (ALL groups must match)
        # Use word boundary matching to avoid substring matches (e.g., "add" in "address")
        import re
        text_words = set(re.findall(r'\b\w+\b', text_lower))

        for group in pattern["required"]:
            # At least ONE keyword from the group must be present as a whole word
            if not any(kw in text_words for kw in group):
                return False, 0.0

        # Check optional keywords (bonus if present)
        optional_matches = 0
        if pattern["optional"]:
            optional_matches = sum(
                1 for kw in pattern["optional"] if kw in text_words
            )

        # Base confidence from pattern
        confidence = pattern["confidence"]

        # Boost confidence if optional keywords matched
        if pattern["optional"] and optional_matches > 0:
            boost = min(0.1, optional_matches * 0.05)
            confidence = min(0.99, confidence + boost)

        return True, confidence

    def match(self, text: str, allowed_intents: Optional[list] = None) -> Optional[Tuple[str, float]]:
        text_lower = text.lower()

        best_match = None
        best_confidence = 0.0

        # Determine which intents to check
        intents_to_check = allowed_intents if allowed_intents else self._compiled_patterns.keys()

        # Try intent patterns
        for intent in intents_to_check:
            patterns = self._compiled_patterns.get(intent, [])
            for pattern in patterns:
                matches, confidence = self._matches_pattern(text_lower, pattern)

                if matches and confidence > best_confidence:
                    best_match = intent
                    best_confidence = confidence

        if best_match:
            return best_match, best_confidence
        return None

    def get_match_explanation(self, text: str, intent: str) -> str:
        text_lower = text.lower()
        patterns = self._compiled_patterns.get(intent, [])

        for pattern in patterns:
            matches, confidence = self._matches_pattern(text_lower, pattern)
            if matches:
                matched_required = []
                for group in pattern["required"]:
                    matched = [kw for kw in group if kw in text_lower]
                    if matched:
                        matched_required.extend(matched)

                matched_optional = [
                    kw for kw in pattern["optional"] if kw in text_lower
                ]

                parts = [f"Matched '{intent}' with confidence {confidence:.2f}",
                         f"Required keywords: {matched_required}"]
                if matched_optional:
                    parts.append(f"Optional keywords: {matched_optional}")

                return " | ".join(parts)

        return f"No match found for '{intent}'"
