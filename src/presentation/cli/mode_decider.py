from enum import Enum


class CLIMode(Enum):
    CLASSIC = "classic"
    NLP = "nlp"

    @classmethod
    def from_string(cls, mode_string: str) -> 'CLIMode':
        return cls.NLP if mode_string == "nlp" else cls.CLASSIC
