import shlex
from typing import Tuple, List


class CommandParser:

    @staticmethod
    def parse(user_input: str) -> Tuple[str, List[str]]:
        try:
            # Use shlex.split() to properly handle quoted strings
            args = shlex.split(user_input)
        except ValueError:
            # If quotes are unbalanced, fall back to simple split
            args = user_input.split()

        if not args:
            return "", []
        command = args[0].lower()
        return command, args[1:]
