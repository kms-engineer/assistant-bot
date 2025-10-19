from typing import Dict

class TemplateParser:
    # Intent list
    VALID_INTENTS = [
        "add_contact", "edit_phone", "edit_email", "edit_address", "delete_contact",
        "list_all_contacts", "search_contacts", "add_birthday", "list_birthdays",
        "add_note", "edit_note", "delete_note", "show_notes", "add_note_tag",
        "remove_note_tag", "search_notes_text", "search_notes_by_tag", "hello", "help", "exit"
    ]

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

        if verbose:
            print("Template Parser initialized (keyword + regex)")

    def parse(
        self,
        user_text: str,
        intent_hint: str = None,
        entities_hint: Dict[str, str] = None
    ) -> Dict:
        result = self._parse_with_templates(user_text, intent_hint, entities_hint)
        result['raw']['source'] = 'template'
        return result

    # Backward compatibility
    def generate_structured_output(
        self,
        user_text: str,
        intent_hint: str = None,
        entities_hint: Dict[str, str] = None
    ) -> Dict:
        return self.parse(user_text, intent_hint, entities_hint)

    def _parse_with_templates(
        self,
        user_text: str,
        intent_hint: str = None,
        entities_hint: Dict = None
    ) -> Dict:
        # Start with entities_hint or empty dict
        entities = entities_hint.copy() if entities_hint else {}

        # Try to extract basic entities from user_text if not already present
        entities = self._extract_basic_entities(user_text, entities)

        result = {
            "intent": intent_hint if intent_hint else "help",
            "confidence": 0.65,  # Moderate confidence for template-based
            "entities": entities,
            "raw": {"spans": [], "probs": {}}
        }

        # Improved keyword-based intent detection
        if not intent_hint or intent_hint == "help":
            text_lower = user_text.lower()

            # Contact operations
            if any(word in text_lower for word in ['add contact', 'new contact', 'create contact', 'save contact', 'add person', 'new person']):
                result['intent'] = 'add_contact'
                result['confidence'] = 0.7

            elif any(word in text_lower for word in ['change email', 'edit email', 'update email', 'email to']):
                result['intent'] = 'edit_email'
                result['confidence'] = 0.7

            elif any(word in text_lower for word in ['change phone', 'edit phone', 'update phone', 'modify phone']):
                result['intent'] = 'edit_phone'
                result['confidence'] = 0.7

            elif any(word in text_lower for word in ['change address', 'edit address', 'update address']):
                result['intent'] = 'edit_address'
                result['confidence'] = 0.7

            elif any(word in text_lower for word in ['delete contact', 'remove contact', 'erase contact']):
                result['intent'] = 'delete_contact'
                result['confidence'] = 0.7

            # Note operations
            elif any(word in text_lower for word in ['add note', 'create note', 'new note', 'make note', 'create a note', 'add a note']):
                result['intent'] = 'add_note'
                result['confidence'] = 0.7

            elif any(word in text_lower for word in ['edit note', 'update note', 'modify note', 'change note']):
                result['intent'] = 'edit_note'
                result['confidence'] = 0.7

            elif any(word in text_lower for word in ['delete note', 'remove note', 'erase note']):
                result['intent'] = 'delete_note'
                result['confidence'] = 0.7

            elif any(word in text_lower for word in ['show notes', 'list notes', 'display notes', 'my notes']):
                result['intent'] = 'show_notes'
                result['confidence'] = 0.7

            # Birthday operations
            elif any(word in text_lower for word in ['show birthday', 'list birthday', 'birthdays for', 'birthdays in', 'birthdays next']):
                result['intent'] = 'list_birthdays'
                result['confidence'] = 0.7

            elif any(word in text_lower for word in ['add birthday', 'set birthday', 'birthday for', 'born on']):
                result['intent'] = 'add_birthday'
                result['confidence'] = 0.7

            # List/Search operations
            elif any(word in text_lower for word in ['show all', 'list all', 'all contacts', 'show contacts', 'list contacts']):
                result['intent'] = 'list_all_contacts'
                result['confidence'] = 0.7

            elif any(word in text_lower for word in ['search contact', 'find contact', 'look up']):
                result['intent'] = 'search_contacts'
                result['confidence'] = 0.65

            elif any(word in text_lower for word in ['search note', 'find note']):
                if 'tag' in text_lower or '#' in user_text:
                    result['intent'] = 'search_notes_by_tag'
                else:
                    result['intent'] = 'search_notes_text'
                result['confidence'] = 0.65

            # Tag operations
            elif any(word in text_lower for word in ['add tag', 'tag note', 'add note tag']):
                result['intent'] = 'add_note_tag'
                result['confidence'] = 0.7

            elif any(word in text_lower for word in ['remove tag', 'delete tag', 'remove note tag']):
                result['intent'] = 'remove_note_tag'
                result['confidence'] = 0.7

            # System commands
            elif any(word in text_lower for word in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'howdy', "what's up", "how's it going", 'how are you', 'sup', 'yo', 'hiya', 'g\'day', 'aloha', 'salutations', 'good day']):
                result['intent'] = 'hello'
                result['confidence'] = 0.9

            elif any(word in text_lower for word in ['help', 'commands', 'what can']):
                result['intent'] = 'help'
                result['confidence'] = 0.8

            elif any(word in text_lower for word in ['exit', 'quit', 'bye', 'goodbye', 'close']):
                result['intent'] = 'exit'
                result['confidence'] = 0.9

        return result

    def _extract_basic_entities(self, user_text: str, existing_entities: Dict) -> Dict:
        import re

        entities = existing_entities.copy()

        # Phone number patterns (various formats)
        if 'phone' not in entities:
            phone_patterns = [
                r'\+?1?\s*\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})',  # US format
                r'\+?(\d{1,3})[\s.-]?\(?(\d{2,4})\)?[\s.-]?(\d{3,4})[\s.-]?(\d{4})',  # International
                r'\b(\d{10})\b',  # 10 digits
                r'\b(\d{3})[\s.-]?(\d{3})[\s.-]?(\d{4})\b',  # Variations
                r'\b(\d{3})[\s.-]?(\d{4})\b',  # Short format 555-9999
                r'\b(\d{7,})\b'  # Any sequence of 7+ digits as fallback
            ]
            for pattern in phone_patterns:
                match = re.search(pattern, user_text)
                if match:
                    # Join all groups to form complete phone
                    phone = ''.join(filter(None, match.groups()))
                    entities['phone'] = phone
                    break

        # Email pattern
        if 'email' not in entities:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            match = re.search(email_pattern, user_text)
            if match:
                entities['email'] = match.group(0)

        # Tag pattern (starts with #)
        if 'tag' not in entities:
            tag_pattern = r'#(\w+)'
            match = re.search(tag_pattern, user_text)
            if match:
                entities['tag'] = '#' + match.group(1)

        # Note ID pattern (numbers after "note", "id", etc.)
        if 'id' not in entities:
            id_patterns = [
                r'note\s+(?:id\s+)?(\d+)',
                r'id\s+(\d+)',
                r'#(\d+)'
            ]
            for pattern in id_patterns:
                match = re.search(pattern, user_text, re.IGNORECASE)
                if match:
                    entities['id'] = match.group(1)
                    break

        # Birthday pattern (dates)
        if 'birthday' not in entities:
            date_patterns = [
                r'\b(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})\b',  # DD/MM/YYYY or MM/DD/YYYY
                r'\b(\d{4})[/.-](\d{1,2})[/.-](\d{1,2})\b',  # YYYY-MM-DD
                r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2}),?\s+(\d{4})\b'  # Month DD, YYYY
            ]
            for pattern in date_patterns:
                match = re.search(pattern, user_text, re.IGNORECASE)
                if match:
                    entities['birthday'] = match.group(0)
                    break

        # Name pattern (capitalized words, typically 2-3 words)
        if 'name' not in entities:
            # Look for capitalized names
            name_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b'
            matches = re.findall(name_pattern, user_text)
            if matches:
                # Filter out common command words
                excluded_words = {'Add', 'Edit', 'Delete', 'Remove', 'Show', 'List', 'Create', 'New', 'Update',
                                 'Change', 'Find', 'Search', 'Contact', 'Note', 'Birthday', 'Tag', 'Email',
                                 'Phone', 'Address', 'Help', 'Exit'}
                for match in matches:
                    # Check if name contains excluded words
                    words = match.split()
                    if not any(word in excluded_words for word in words):
                        entities['name'] = match
                        break

        # Address pattern (street address indicators)
        if 'address' not in entities:
            # Look for common address patterns
            address_patterns = [
                r'\d+\s+[A-Z][a-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)',
                r'from\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:,\s*[A-Z][a-z]+)?)',  # "from City, Country"
            ]
            for pattern in address_patterns:
                match = re.search(pattern, user_text, re.IGNORECASE)
                if match:
                    if 'from' in pattern:
                        entities['address'] = match.group(1)
                    else:
                        entities['address'] = match.group(0)
                    break

        # Note text extraction (for add_note intent)
        # This is tricky - try to extract quoted text or text after keywords
        if 'note_text' not in entities:
            # Check for quoted text
            quoted_patterns = [
                r'"([^"]+)"',  # Double quotes
                r"'([^']+)'",  # Single quotes
            ]
            for pattern in quoted_patterns:
                match = re.search(pattern, user_text)
                if match:
                    entities['note_text'] = match.group(1)
                    break

            # If no quotes, try to extract text after "note" keyword
            if 'note_text' not in entities:
                note_patterns = [
                    r'(?:add|create|new)\s+note\s+["\']?(.+?)["\']?$',  # add/create note <text>
                    r'(?:edit|update)\s+note\s+\d+\s+(.+)$',  # edit note 5 <text>
                    r'note:\s*(.+)$',  # note: <text>
                    r'note\s+(?:id\s+)?\d+\s+(.+)$'  # note 5 <text> or note id 5 <text>
                ]
                for pattern in note_patterns:
                    match = re.search(pattern, user_text, re.IGNORECASE)
                    if match:
                        text = match.group(1).strip()
                        # Clean up
                        text = text.strip('"\' ')
                        if text:
                            entities['note_text'] = text
                        break

        return entities
