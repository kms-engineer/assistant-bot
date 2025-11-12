from typing import Dict
from src.config import IntentConfig, ConfidenceConfig, RegexPatterns, EntityConfig
from src.config.keyword_map import GREETING_KEYWORDS


class TemplateParser:

    def __init__(self):
        pass

    def parse(
        self,
        user_text: str,
        intent_hint: str | None = None,
        entities_hint: Dict[str, str] | None = None,
    ) -> Dict:
        result = self._parse_with_templates(user_text, intent_hint, entities_hint)
        result["raw"]["source"] = "template"
        return result

    # Backward compatibility
    def generate_structured_output(
        self,
        user_text: str,
        intent_hint: str | None = None,
        entities_hint: Dict[str, str] | None = None,
    ) -> Dict:
        return self.parse(user_text, intent_hint, entities_hint)

    def _parse_with_templates(
        self, user_text: str, intent_hint: str | None, entities_hint: Dict | None
    ) -> Dict:
        # Start with entities_hint or empty dict
        entities = entities_hint.copy() if entities_hint else {}

        # Try to extract basic entities from user_text if not already present
        entities = self._extract_basic_entities(user_text, entities)

        result = {
            "intent": intent_hint if intent_hint else IntentConfig.DEFAULT_INTENT,
            "confidence": ConfidenceConfig.TEMPLATE_BASE_CONFIDENCE,
            "entities": entities,
            "raw": {"spans": [], "probs": {}},
        }

        # Keyword-based intent detection using KEYWORD_MAP
        if not intent_hint or intent_hint == IntentConfig.DEFAULT_INTENT:
            text_lower = user_text.lower()

            # Check for greetings first (highest confidence, with extended keywords)
            if any(keyword in text_lower for keyword in GREETING_KEYWORDS):
                result["intent"] = "hello"
                result["confidence"] = ConfidenceConfig.TEMPLATE_HELLO_CONFIDENCE
                return result

            # Check KEYWORD_MAP for all other intents
            for intent, keywords in IntentConfig.KEYWORD_MAP.items():
                if any(keyword in text_lower for keyword in keywords):
                    # Set confidence based on intent type
                    if intent == "exit":
                        result["confidence"] = ConfidenceConfig.TEMPLATE_EXIT_CONFIDENCE
                    elif intent == "help":
                        result["confidence"] = ConfidenceConfig.TEMPLATE_HELP_CONFIDENCE
                    elif intent in ["search_contacts", "search_notes_text"]:
                        result["confidence"] = ConfidenceConfig.TEMPLATE_BASE_CONFIDENCE
                    else:
                        result["confidence"] = ConfidenceConfig.TEMPLATE_HIGH_CONFIDENCE

                    result["intent"] = intent
                    break

            # Special case: search_notes - check if it's by tag or text
            if result["intent"] == "search_notes_text":
                if "tag" in text_lower or "#" in user_text:
                    result["intent"] = "search_notes_by_tag"

        return result

    @staticmethod
    def _extract_basic_entities(user_text: str, existing_entities: Dict) -> Dict:
        import re

        entities = existing_entities.copy()

        # Phone number patterns (try multiple formats)
        if "phone" not in entities:
            for pattern in RegexPatterns.TEMPLATE_PHONE_PATTERNS:
                match = re.search(pattern, user_text)
                if match:
                    # Join all groups to form complete phone
                    phone = "".join(filter(None, match.groups()))
                    entities["phone"] = phone
                    break

        # Email pattern
        if "email" not in entities:
            match = re.search(RegexPatterns.EMAIL_PATTERN, user_text)
            if match:
                entities["email"] = match.group(0)

        # Tag pattern
        if "tag" not in entities:
            match = re.search(RegexPatterns.TAG_PATTERN, user_text)
            if match:
                entities["tag"] = match.group(0)

        # Note ID pattern
        if "id" not in entities:
            for pattern in RegexPatterns.TEMPLATE_ID_PATTERNS:
                match = re.search(pattern, user_text, re.IGNORECASE)
                if match:
                    entities["id"] = match.group(1)
                    break

        # Birthday pattern (dates)
        if "birthday" not in entities:
            match = re.search(
                RegexPatterns.BIRTHDAY_PATTERN_COMBINED, user_text, re.IGNORECASE
            )
            if match:
                entities["birthday"] = match.group(0)

        # Name pattern (capitalized words)
        if "name" not in entities:
            matches = re.findall(RegexPatterns.NAME_FULL_PATTERN, user_text)
            if matches:
                # Filter out command words
                for match in matches:
                    words = match.split()
                    if not any(
                        word in EntityConfig.NAME_EXCLUDED_WORDS for word in words
                    ):
                        entities["name"] = match
                        break

        # Address patterns
        if "address" not in entities:
            # Street address
            match = re.search(
                RegexPatterns.TEMPLATE_ADDRESS_STREET_FULL, user_text, re.IGNORECASE
            )
            if match:
                entities["address"] = match.group(0)
            else:
                # "from City, Country" format
                match = re.search(
                    RegexPatterns.TEMPLATE_ADDRESS_FROM_PATTERN,
                    user_text,
                    re.IGNORECASE,
                )
                if match:
                    entities["address"] = match.group(1)

        # Note text extraction
        if "note_text" not in entities:
            # Check for quoted text first
            for pattern in RegexPatterns.QUOTED_PATTERNS:
                match = re.search(pattern, user_text)
                if match:
                    entities["note_text"] = match.group(1)
                    break

            # If no quotes, try note command patterns
            if "note_text" not in entities:
                for pattern in RegexPatterns.TEMPLATE_NOTE_TEXT_PATTERNS:
                    match = re.search(pattern, user_text, re.IGNORECASE)
                    if match:
                        text = match.group(1).strip().strip("\"' ")
                        if text:
                            entities["note_text"] = text
                        break

        return entities
