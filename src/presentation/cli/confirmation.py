"""
Reusable confirmation prompt module for destructive actions.

This module provides a consistent way to ask for user confirmation
before performing destructive operations like deleting contacts or
overwriting data.
"""

# Constants for valid responses
_VALID_YES = ('y', 'yes')
_VALID_NO = ('n', 'no')
_ERROR_MESSAGE = "Please answer 'y' or 'n'."


def confirm_action(prompt, default=False):
    """
    Prompts the user for confirmation (y/n) and returns the result.

    Keeps asking until a valid response ('y' or 'n') is provided.
    Uses safe defaults (False/No) for destructive actions.

    Args:
        prompt: The message to display to the user
        default: Default value if user presses Enter (False = 'n', True = 'y')
                 Defaults to False for safety

    Returns:
        True if user confirms (y/yes), False otherwise (n/no)

    Raises:
        EOFError: If input stream is closed (e.g., in non-interactive mode)
        KeyboardInterrupt: If user interrupts with Ctrl+C

    Examples:
        >>> confirm_action("Delete contact John?")
        Delete contact John? (y/n) [n]: y
        True

        >>> confirm_action("Load file?", default=True)
        Load file? (y/n) [y]:
        True

        >>> confirm_action("Delete contact?")
        Delete contact? (y/n) [n]:
        False
    """
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
