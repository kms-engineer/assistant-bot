from typing import Dict
from src.domain.validators.intent_validator import IntentValidator


class ValidationAdapter:
    def __init__(self):
        self.validator = IntentValidator()

    def validate(self, entities: Dict, intent: str) -> Dict:
        result = self.validator.validate_for_intent(entities, intent)

        needs_fallback = not result["valid"]

        return {
            "valid": result["valid"],
            "missing": result["missing"],
            "required": result["required"],
            "optional": result.get("optional", []),
            "has_optional": result.get("has_optional", False),
            "needs_fallback": needs_fallback,
        }
