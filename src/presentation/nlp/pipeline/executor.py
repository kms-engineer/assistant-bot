from typing import List
from .base import PipelineStage, NLPContext


class NLPPipeline:
    def __init__(self, stages: List[PipelineStage]):
        self.stages = stages

    def execute(self, user_text: str) -> dict:
        context = NLPContext(user_text=user_text)

        for stage in self.stages:
            if not stage.should_skip(context):
                context = stage.execute(context)

        return {
            "intent": context.intent,
            "intent_confidence": context.intent_confidence,  # Include as intent_confidence
            "confidence": context.intent_confidence,  # Keep for backward compatibility
            "entities": context.entities,
            "entity_confidences": context.entity_confidences,
            "validation": context.validation,
            "source": context.source,
            "metadata": context.metadata,  # Include metadata (category, etc.)
            "raw": {
                "source": context.source,
                "entity_confidences": context.entity_confidences,
            },
        }

    def shutdown(self):
        for stage in self.stages:
            if hasattr(stage, "shutdown"):
                stage.shutdown()
