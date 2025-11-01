# Constants for valid responses
_VALID_YES = ('y', 'yes')
_VALID_NO = ('n', 'no')
_ERROR_MESSAGE = "Please answer 'y' or 'n'."


def confirm_action(prompt, default=False):
    default_indicator = "[y]" if default else "[n]"
    full_prompt = f"{prompt} (y/n) {default_indicator}: "

    while True:
        try:
            response = input(full_prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            # Handle non-interactive mode or Ctrl+C gracefully
            print()  # New line for clean output
            return False  # Safe default for destructive actions

        # Handle empty response (use default)
        if not response:
            return default

        # Handle valid responses
        if response in _VALID_YES:
            return True

        if response in _VALID_NO:
            return False

        # Invalid response - loop continues
        print(_ERROR_MESSAGE)
