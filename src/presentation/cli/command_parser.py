from typing import Tuple, List


class CommandParser:

    @staticmethod
    def parse(user_input: str) -> Tuple[str, List[str]]:
        args = user_input.split()
        if not args:
            return "", []
        command = args[0].lower()
        return command, args[1:]
