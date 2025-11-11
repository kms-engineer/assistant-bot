from ..base import PipelineStage, NLPContext
from ...post_rules import PostProcessingRules


class PostProcessStage(PipelineStage):
    def __init__(self, post_processor: PostProcessingRules):
        super().__init__("post_process")
        self.processor = post_processor

    def execute(self, context: NLPContext) -> NLPContext:
        processed = self.processor.process(
            context.entities, context.intent, context.user_text
        )
        validation = self.processor.validate_entities_for_intent(
            processed, context.intent
        )

        if "_validation_errors" in processed:
            validation["errors"] = processed.pop("_validation_errors")
        else:
            validation["errors"] = []

        context.entities = processed
        context.validation = validation
        return context
