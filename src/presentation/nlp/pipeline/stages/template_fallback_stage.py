from ..base import PipelineStage, NLPContext
from ...template_parser import TemplateParser
from src.config import NLPConfig, EntityConfig


class TemplateFallbackStage(PipelineStage):
    def __init__(self, template_parser: TemplateParser):
        super().__init__("template_fallback")
        self.parser = template_parser

    def should_skip(self, context: NLPContext) -> bool:
        is_valid = context.validation.get('valid', False)
        high_conf = context.intent_confidence >= NLPConfig.INTENT_CONFIDENCE_THRESHOLD
        return is_valid or high_conf

    def execute(self, context: NLPContext) -> NLPContext:
        if context.verbose:
            print("[Template] Using template parser")

        result = self.parser.generate_structured_output(
            context.user_text,
            intent_hint=context.intent,
            entities_hint=context.entities
        )

        if result.get('confidence', 0) >= EntityConfig.ENTITY_MERGE_THRESHOLD:
            context.intent = result['intent']
            context.intent_confidence = result['confidence']
            context.entities = result['entities']
            context.source = "template"

        return context
