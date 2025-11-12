from ..base import PipelineStage, NLPContext
from ...span_extractor import SpanExtractor
from ...validation_adapter import ValidationAdapter
from ...entity_merger import EntityMerger


class RegexFallbackStage(PipelineStage):
    def __init__(self, span_extractor: SpanExtractor, validator: ValidationAdapter):
        super().__init__("regex_fallback")
        self.span_extractor = span_extractor
        self.validator = validator

    def should_skip(self, context: NLPContext) -> bool:
        # Skip if validation passed AND we have at least one entity
        if not context.validation.get("valid", False):
            return False

        # Check if we have any non-None entities
        entities = context.entities or {}
        has_entities = any(v is not None for v in entities.values())

        # Only skip if validation passed AND we have entities
        return has_entities

    def execute(self, context: NLPContext) -> NLPContext:
        entities_regex, spans, probs = self.span_extractor.extract(
            context.user_text, intent=context.intent
        )

        merged = EntityMerger.merge(
            entities_regex, context.entities, probs, context.entity_confidences
        )
        context.entities = merged
        context.source = "ner+regex"

        context.validation = self.validator.validate(context.entities, context.intent)
        return context
