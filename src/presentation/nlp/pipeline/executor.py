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
            'intent': context.intent,
            'confidence': context.intent_confidence,
            'entities': context.entities,
            'validation': context.validation,
            'raw': {
                'source': context.source,
                'entity_confidences': context.entity_confidences
            }
        }

    def shutdown(self):
        for stage in self.stages:
            if hasattr(stage, 'shutdown'):
                stage.shutdown()
