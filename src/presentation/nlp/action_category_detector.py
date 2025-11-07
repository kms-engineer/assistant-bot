from typing import Optional, Tuple
from src.config.nlp_config import NLPConfig


class ActionCategoryDetector:

    def __init__(self):
        self.category_keywords = NLPConfig.CATEGORY_KEYWORDS

    def detect(self, text: str) -> Tuple[Optional[str], float]:
        text_lower = text.lower()
        words = set(text_lower.split())

        # Count matches for each category
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            matches = len(keywords.intersection(words))
            if matches > 0:
                # Confidence based on number of matches
                # 1 match = 0.7, 2 matches = 0.85, 3+ matches = 0.95
                if matches >= 3:
                    confidence = 0.95
                elif matches == 2:
                    confidence = 0.85
                else:
                    confidence = 0.7
                category_scores[category] = confidence

        # Return category with highest confidence
        if category_scores:
            best_category = max(category_scores.items(), key=lambda x: x[1])
            return best_category[0], best_category[1]

        return None, 0.0

    def get_allowed_intents(self, category: Optional[str]) -> list:
        if category is None:
            return []
        return NLPConfig.CATEGORY_TO_INTENTS.get(category, [])
