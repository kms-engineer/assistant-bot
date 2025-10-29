from ..base import PipelineStage, NLPContext
from ...validation_adapter import ValidationAdapter


class ValidationStage(PipelineStage):
    def __init__(self, validator: ValidationAdapter):
        super().__init__("validation")
        self.validator = validator

    def execute(self, context: NLPContext) -> NLPContext:
        context.validation = self.validator.validate(context.entities, context.intent)
        if context.verbose:
            print(f"[Validation] Valid: {context.validation['valid']}, Missing: {context.validation['missing']}")
        return context
