from typing import Dict, Tuple, List, Union
from .intent_classifier import IntentClassifier
from .ner_model import NERModel
from .span_extractor import SpanExtractor
from .template_parser import TemplateParser
from .post_rules import PostProcessingRules
from .validation_adapter import ValidationAdapter
from .pipeline.executor import NLPPipeline
from .pipeline.stages import (
    ParallelIntentNERStage, ValidationStage, RegexFallbackStage,
    TemplateFallbackStage, PostProcessStage
)
from src.config import IntentConfig
from src.config.command_args_config import CommandArgsConfig


class HybridNLP:
    def __init__(
        self,
        intent_model_path: str = None,
        ner_model_path: str = None,
        default_region: str = "US",
        use_parallel: bool = True
    ):
        print("Initializing NLP Pipeline")
        if use_parallel:
            print("Parallel: ENABLED (Intent+NER)\n")

        intent_classifier = IntentClassifier(model_path=intent_model_path)
        ner_model = NERModel(model_path=ner_model_path)
        span_extractor = SpanExtractor()
        template_parser = TemplateParser(verbose=False)
        post_processor = PostProcessingRules(default_region=default_region)
        validator = ValidationAdapter()

        stages = [
            ParallelIntentNERStage(intent_classifier, ner_model, use_parallel),
            ValidationStage(validator),
            RegexFallbackStage(span_extractor, validator),
            TemplateFallbackStage(template_parser),
            PostProcessStage(post_processor)
        ]

        self.pipeline = NLPPipeline(stages)

    def process(self, user_text: str, verbose: bool = False) -> Dict:
        result = self.pipeline.execute(user_text, verbose)

        if verbose:
            print("=" * 60)
            print(f"Result: {result['intent']} (conf: {result['confidence']:.2f})")
            print(f"Entities: {result['entities']}")
            print(f"Valid: {result['validation']['valid']}")

        return result

    def shutdown(self):
        self.pipeline.shutdown()

    def __del__(self):
        self.shutdown()

    @staticmethod
    def get_command_args(nlp_result: Dict) -> Union[Tuple[str, List], Tuple[str, Dict]]:
        intent = nlp_result['intent']
        entities = nlp_result['entities']
        validation = nlp_result.get('validation', {})

        command = IntentConfig.INTENT_TO_COMMAND_MAP.get(intent, 'help')

        # Return pipeline if optional entities present (for pipeline execution)
        if validation.get('has_optional', False) and intent not in CommandArgsConfig.SKIP_PIPELINE_INTENTS:
            return 'pipeline', nlp_result

        # Build args using config
        builder = CommandArgsConfig.INTENT_ARG_BUILDERS.get(intent, lambda e: [])
        args = builder(entities)

        return command, args
