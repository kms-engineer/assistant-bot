from concurrent.futures import ThreadPoolExecutor
from ..base import PipelineStage, NLPContext
from ...intent_classifier import IntentClassifier
from ...ner_model import NERModel


class ParallelIntentNERStage(PipelineStage):
    def __init__(self, intent_classifier: IntentClassifier, ner_model: NERModel, use_parallel: bool = True):
        super().__init__("intent_ner")
        self.intent_classifier = intent_classifier
        self.ner_model = ner_model
        self.executor = ThreadPoolExecutor(max_workers=2) if use_parallel else None

    def execute(self, context: NLPContext) -> NLPContext:
        if self.executor:
            intent_future = self.executor.submit(self.intent_classifier.predict, context.user_text)
            ner_future = self.executor.submit(self.ner_model.extract_entities, context.user_text, context.verbose)
            context.intent, context.intent_confidence = intent_future.result()
            context.entities, context.entity_confidences = ner_future.result()
        else:
            context.intent, context.intent_confidence = self.intent_classifier.predict(context.user_text)
            context.entities, context.entity_confidences = self.ner_model.extract_entities(context.user_text, context.verbose)

        context.source = "ner"
        if context.verbose:
            print(f"[Intent+NER] {context.intent} (conf: {context.intent_confidence:.2f}), entities: {context.entities}")
        return context

    def shutdown(self):
        if self.executor:
            self.executor.shutdown(wait=True)
