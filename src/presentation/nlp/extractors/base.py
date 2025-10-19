from dataclasses import dataclass
from enum import Enum


class ExtractionStrategy(Enum):
    LIBRARY = "library"
    REGEX = "regex"
    ML = "ml"
    HEURISTIC = "heuristic"


@dataclass
class Entity:
    text: str
    start: int
    end: int
    entity_type: str
    confidence: float = 1.0
    strategy: ExtractionStrategy = ExtractionStrategy.REGEX


STOP_WORDS = {
    'Add', 'Create', 'Save', 'Update', 'Change', 'Edit', 'Delete', 'Remove',
    'Set', 'Get', 'Show', 'List', 'Search', 'Find', 'Display', 'New',
    'Person', 'Contact', 'Entry', 'Record', 'User', 'Client', 'Member',
    'Phone', 'Email', 'Address', 'Birthday', 'Note', 'Tag', 'Info',
    'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December',
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
    'Please', 'Can', 'Could', 'Would', 'Should', 'Will', 'May', 'Might',
    'Suite', 'Apt', 'Apartment', 'Unit', 'Building', 'Floor', 'Room'
}


def is_stop_word(word: str) -> bool:
    return word in STOP_WORDS
