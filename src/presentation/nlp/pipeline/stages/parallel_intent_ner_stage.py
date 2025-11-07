from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, Optional
from ..base import PipelineStage, NLPContext
from ...intent_classifier import IntentClassifier
from ...action_category_detector import ActionCategoryDetector
from ...ner_model import NERModel
from ...keyword_intent_matcher import KeywordIntentMatcher
from src.config.nlp_config import NLPConfig


class ParallelIntentNERStage(PipelineStage):

    def __init__(
        self,
        intent_classifier: IntentClassifier,
        ner_model: NERModel,
        use_parallel: bool = True,
        use_category_validation: bool = True,
        use_keyword_matcher: bool = True
    ):
        super().__init__("intent_ner")
        self.intent_classifier = intent_classifier
        self.category_detector = ActionCategoryDetector()
        self.ner_model = ner_model
        self.use_category_validation = use_category_validation
        self.use_keyword_matcher = use_keyword_matcher

        # Initialize keyword matcher if enabled
        self.keyword_matcher = KeywordIntentMatcher() if use_keyword_matcher else None

        # Thread pool for parallel execution
        if use_parallel:
            # 3 workers: intent, category, keyword matching
            self.executor = ThreadPoolExecutor(max_workers=3)
        else:
            self.executor = None

    def execute(self, context: NLPContext) -> NLPContext:
        user_text = context.user_text

        if self.use_keyword_matcher:
            return self._execute_with_fallback(context, user_text)
        else:
            return self._execute_classifier_only(context, user_text)

    def _execute_classifier_only(self, context: NLPContext, user_text: str) -> NLPContext:
        if self.executor:
            # Parallel: intent + category + NER
            intent_future = self.executor.submit(
                self.intent_classifier.predict,
                user_text
            )
            category_future = self.executor.submit(
                self.category_detector.detect,
                user_text
            )
            ner_future = self.executor.submit(
                self.ner_model.extract_entities,
                user_text
            )

            # Get results
            ml_intent, ml_conf = intent_future.result()
            category, cat_conf = category_future.result()
            entities, entity_confidences = ner_future.result()
        else:
            # Sequential
            ml_intent, ml_conf = self.intent_classifier.predict(user_text)
            category, cat_conf = self.category_detector.detect(user_text)
            entities, entity_confidences = self.ner_model.extract_entities(user_text)

        # Validate intent belongs to detected category
        final_intent, final_conf, source = self._validate_and_correct_intent(
            user_text, ml_intent, ml_conf, category
        )

        # Update context
        context.intent = final_intent
        context.intent_confidence = final_conf
        context.entities = entities
        context.entity_confidences = entity_confidences
        context.source = source

        # Store category in metadata
        context.metadata["category"] = category
        context.metadata["category_confidence"] = cat_conf
        context.metadata["ml_intent"] = ml_intent
        context.metadata["ml_confidence"] = ml_conf

        return context

    def _execute_with_fallback(self, context: NLPContext, user_text: str) -> NLPContext:
        if self.executor:
            # Parallel: intent + category + keyword
            intent_future = self.executor.submit(
                self.intent_classifier.predict,
                user_text
            )
            category_future = self.executor.submit(
                self.category_detector.detect,
                user_text
            )
            keyword_future = self.executor.submit(
                self._keyword_match,
                user_text
            )

            # Get results
            ml_intent, ml_conf = intent_future.result()
            category, cat_conf = category_future.result()
            keyword_result = keyword_future.result()
        else:
            # Sequential
            ml_intent, ml_conf = self.intent_classifier.predict(user_text)
            category, cat_conf = self.category_detector.detect(user_text)
            keyword_result = self._keyword_match(user_text)

        # Select best intent with category validation
        final_intent, final_confidence, source = self._select_best_intent(
            user_text,
            ml_intent, ml_conf,
            keyword_result,
            category
        )

        # Run NER with intent guidance
        entities, entity_confidences = self.ner_model.extract_entities(
            user_text,
            intent=final_intent
        )

        # Update context
        context.intent = final_intent
        context.intent_confidence = final_confidence
        context.entities = entities
        context.entity_confidences = entity_confidences
        context.source = source

        # Store metadata
        context.metadata["category"] = category
        context.metadata["category_confidence"] = cat_conf
        context.metadata["ml_intent"] = ml_intent
        context.metadata["ml_confidence"] = ml_conf

        if keyword_result:
            context.metadata["keyword_intent"] = keyword_result[0]
            context.metadata["keyword_confidence"] = keyword_result[1]

        return context

    def _validate_and_correct_intent(
        self,
        user_text: str,
        ml_intent: str,
        ml_conf: float,
        category: Optional[str]
    ) -> Tuple[str, float, str]:
        if not self.use_category_validation or not category:
            return ml_intent, ml_conf, "ml_classifier"

        # Get allowed intents for this category
        allowed_intents = self.category_detector.get_allowed_intents(category)

        # Check if ML intent matches category
        if ml_intent in allowed_intents:
            return ml_intent, ml_conf, "ml_classifier"

        # Intent doesn't match category - try keyword matcher
        if self.keyword_matcher:
            keyword_result = self._keyword_match_in_category(user_text, allowed_intents)
            if keyword_result:
                keyword_intent, keyword_conf = keyword_result
                return keyword_intent, keyword_conf, "keyword_corrected"

        # No better option found - return ML result but with lower confidence
        return ml_intent, ml_conf * 0.5, "ml_classifier_uncategorized"

    def _select_best_intent(
        self,
        user_text: str,
        ml_intent: str,
        ml_confidence: float,
        keyword_result: Optional[Tuple[str, float]],
        category: Optional[str]
    ) -> Tuple[str, float, str]:
        # Get allowed intents for category
        allowed_intents = None
        if self.use_category_validation and category:
            allowed_intents = self.category_detector.get_allowed_intents(category)

        # Check if ML intent matches category
        ml_matches_category = (
            not allowed_intents or
            ml_intent in allowed_intents
        )

        # No keyword result - validate and return ML
        if not keyword_result:
            if ml_matches_category:
                return ml_intent, ml_confidence, "ml_classifier"
            else:
                # Try to find better match in category
                if self.keyword_matcher and allowed_intents:
                    category_match = self._keyword_match_in_category(user_text, allowed_intents)
                    if category_match:
                        return category_match[0], category_match[1], "keyword_corrected"
                # No better option
                return ml_intent, ml_confidence * 0.5, "ml_classifier_uncategorized"

        keyword_intent, keyword_confidence = keyword_result

        # Check if keyword intent matches category
        keyword_matches_category = (
            not allowed_intents or
            keyword_intent in allowed_intents
        )

        # Case 1: Both match category - choose by confidence
        if ml_matches_category and keyword_matches_category:
            # Both agree on the same intent
            if ml_intent == keyword_intent:
                if keyword_confidence > ml_confidence:
                    return keyword_intent, keyword_confidence, "keyword"
                else:
                    return ml_intent, ml_confidence, "ml_classifier"

            # They disagree - check confidence difference
            confidence_diff = keyword_confidence - ml_confidence

            # If keyword has significantly higher confidence, trust keyword
            if (keyword_confidence >= NLPConfig.KEYWORD_HIGH_CONFIDENCE_THRESHOLD and
                confidence_diff > 0):
                return keyword_intent, keyword_confidence, "keyword"

            # If ML has significantly higher confidence, trust ML
            if ml_confidence >= NLPConfig.ML_LOW_CONFIDENCE_THRESHOLD:
                return ml_intent, ml_confidence, "ml_classifier"

            # Both have similar confidence - prefer keyword if it's high
            if keyword_confidence >= NLPConfig.KEYWORD_HIGH_CONFIDENCE_THRESHOLD:
                return keyword_intent, keyword_confidence, "keyword"

            # Fallback to ML
            return ml_intent, ml_confidence, "ml_classifier"

        # Case 2: Only ML matches category
        if ml_matches_category and not keyword_matches_category:
            # If keyword has very high confidence (>=0.9) and ML is low (<0.5), prefer keyword
            if keyword_confidence >= 0.9 and ml_confidence < 0.5:
                return keyword_intent, keyword_confidence, "keyword_high_confidence"
            return ml_intent, ml_confidence, "ml_classifier"

        # Case 3: Only keyword matches category
        if keyword_matches_category and not ml_matches_category:
            return keyword_intent, keyword_confidence, "keyword_corrected"

        # Case 4: Neither matches category - prefer higher confidence
        if ml_confidence > keyword_confidence:
            return ml_intent, ml_confidence * 0.7, "ml_classifier_uncategorized"
        else:
            return keyword_intent, keyword_confidence * 0.7, "keyword_uncategorized"

    def _keyword_match(self, text: str) -> Optional[Tuple[str, float]]:
        if not self.keyword_matcher:
            return None
        return self.keyword_matcher.match(text)

    def _keyword_match_in_category(
        self,
        text: str,
        allowed_intents: list
    ) -> Optional[Tuple[str, float]]:
        if not self.keyword_matcher:
            return None
        return self.keyword_matcher.match(text, allowed_intents=allowed_intents)

    def shutdown(self):
        if self.executor:
            self.executor.shutdown(wait=True)
