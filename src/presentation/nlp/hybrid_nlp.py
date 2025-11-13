from typing import Dict, Tuple, List, Union, Optional
from .intent_classifier import IntentClassifier
from .ner_model import NERModel
from .span_extractor import SpanExtractor
from .template_parser import TemplateParser
from .post_rules import PostProcessingRules
from .validation_adapter import ValidationAdapter
from .pipeline.executor import NLPPipeline
from .pipeline.stages import (
    ParallelIntentNERStage,
    ValidationStage,
    RegexFallbackStage,
    TemplateFallbackStage,
    PostProcessStage,
)
from src.config import IntentConfig
from src.config.command_args_config import CommandArgsConfig


class HybridNLP:

    def __init__(
        self,
        intent_model_path: Optional[str] = None,
        ner_model_path: Optional[str] = None,
        default_region: str = "US",
        use_parallel: bool = True,
        use_category_validation: bool = True,
        use_keyword_matcher: bool = True,
    ):
        # Initialize models
        intent_classifier = IntentClassifier(model_path=intent_model_path)
        ner_model = NERModel(model_path=ner_model_path)
        span_extractor = SpanExtractor()
        template_parser = TemplateParser()
        post_processor = PostProcessingRules(default_region=default_region)
        validator = ValidationAdapter()

        # Create pipeline with stages
        stages = [
            # Stage 1: Intent+NER (with category validation and keyword fallback)
            ParallelIntentNERStage(
                intent_classifier,
                ner_model,
                use_parallel=use_parallel,
                use_category_validation=use_category_validation,
                use_keyword_matcher=use_keyword_matcher,
            ),
            # Stage 2: Validation
            ValidationStage(validator),
            # Stage 3: Regex Fallback
            RegexFallbackStage(span_extractor, validator),
            # Stage 4: Template Fallback
            TemplateFallbackStage(template_parser),
            # Stage 5: Post-Processing
            PostProcessStage(post_processor),
        ]

        self.pipeline = NLPPipeline(stages)

    def process(self, user_text: str) -> Dict:
        return self.pipeline.execute(user_text)

    def shutdown(self):
        if self.pipeline:
            self.pipeline.shutdown()

    def __del__(self):
        self.shutdown()

    @staticmethod
    def get_command_args(nlp_result: Dict) -> Tuple[str, List]:
        intent = nlp_result["intent"]
        entities = nlp_result["entities"]

        # Map intent to command name
        command = IntentConfig.INTENT_TO_COMMAND_MAP.get(intent, intent)

        # Get argument builder for this intent
        arg_builder = CommandArgsConfig.INTENT_ARG_BUILDERS.get(intent)

        if not arg_builder:
            return command, []

        # Call the builder function to get args
        args = arg_builder(entities)

        return command, args

    def get_available_intents(self) -> List[str]:
        return list(IntentConfig.INTENT_TO_COMMAND_MAP.keys())

    def get_category_for_intent(self, intent: str) -> str:
        from src.config.nlp_config import NLPConfig

        # Find category by CATEGORY_TO_INTENTS mapping
        for category, intents in NLPConfig.CATEGORY_TO_INTENTS.items():
            if intent in intents:
                return category

        return "other"
