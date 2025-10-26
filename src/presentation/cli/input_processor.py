from difflib import get_close_matches
from .command_parser import CommandParser
from .command_handler import CommandHandler
from .regex_gate import RegexCommandGate


def process_classic_input(user_input: str, parser: CommandParser, handler: CommandHandler) -> str:
    command, args = parser.parse(user_input)
    return handler.handle(command, args)


def process_nlp_input(user_input: str, regex_gate: RegexCommandGate, handler: CommandHandler, nlp_manager=None) -> str:
    # First try regex matching
    parsed = regex_gate.match(user_input)
    if parsed:
        command, args = parsed
        return handler.handle(command, args)

    # If regex fails, try NLP processing
    if nlp_manager and nlp_manager.is_ready():
        try:
            verbose = False
            nlp_result = nlp_manager.process_input(user_input, verbose=verbose)

            if nlp_result is None:
                # NLP processor not available - suggest similar commands
                return _get_nlp_failure_message(user_input, handler)

            # Check confidence - if very low, suggest commands
            confidence = nlp_result.get('confidence', 0.0)
            LOW_CONFIDENCE_THRESHOLD = 0.55  # If confidence < 0.55, suggest alternatives

            if confidence < LOW_CONFIDENCE_THRESHOLD:
                # Low confidence result - might be wrong, suggest alternatives
                suggestion_msg = _get_nlp_failure_message(user_input, handler)
                return f"Low confidence understanding (confidence: {confidence:.2f}).\n{suggestion_msg}"

            # Check if validation passed
            if nlp_result.get('validation', {}).get('valid', False):
                command, args = nlp_manager.get_command_args(nlp_result)
                return handler.handle(command, args)
            else:
                # Show what was understood and what's missing
                missing = nlp_result.get('validation', {}).get('missing', [])
                errors = nlp_result.get('validation', {}).get('errors', [])

                response = f"I understood your intent as '{nlp_result['intent']}'"
                if nlp_result['entities']:
                    response += f" with: {nlp_result['entities']}"

                if missing:
                    response += f"\n\nMissing required information: {', '.join(missing)}"
                if errors:
                    response += f"\n\nValidation errors: {'; '.join(errors)}"

                return response
        except Exception as e:
            # NLP processing failed - suggest similar commands
            return _get_nlp_failure_message(user_input, handler, error=str(e))

    # NLP manager not available
    return _get_nlp_failure_message(user_input, handler)


def _get_nlp_failure_message(user_input: str, handler: CommandHandler, error: str = None) -> str:
    # Get example phrases for NLP
    examples = handler.get_nlp_command_examples()

    # Try to find similar command examples
    suggestions = get_close_matches(user_input.lower(), examples, n=1, cutoff=0.6)

    base_message = "Could not understand the command."
    if error:
        base_message = f"NLP processing error: {error}"

    if suggestions:
        return f"{base_message}\n\nDid you mean: \"{suggestions[0]}\"?\n\nType 'help' for all available commands."
    else:
        return f"{base_message}\n\nPlease try rephrasing or type 'help' for available commands."