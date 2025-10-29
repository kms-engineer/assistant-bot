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
        return context.validation.get('valid', False)

    def execute(self, context: NLPContext) -> NLPContext:
        entities_regex, spans, probs = self.span_extractor.extract(context.user_text)
        if context.verbose:
            print(f"[Regex] Extracted: {entities_regex}")

        merged = EntityMerger.merge(entities_regex, context.entities, probs, context.entity_confidences)
        context.entities = merged
        context.source = "ner+regex"

        context.validation = self.validator.validate(context.entities, context.intent)
        return context
