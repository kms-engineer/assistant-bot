from typing import List, Dict, Callable


class CommandArgsConfig:

    @staticmethod
    def _get_fields(entities: Dict, *fields) -> List[str]:
        return [
            entities[f] for f in fields if f in entities and entities[f] is not None
        ]

    @staticmethod
    def _get_first(entities: Dict, *fields) -> List[str]:
        for field in fields:
            if field in entities and entities[field] is not None:
                return [entities[field]]
        return []

    @staticmethod
    def _with_default(entities: Dict, field: str, default: str) -> List[str]:
        return [str(entities.get(field, default))]

    INTENT_ARG_BUILDERS: Dict[str, Callable] = {
        "add_contact": lambda e: CommandArgsConfig._get_fields(e, "name", "phone"),
        "edit_phone": lambda e: CommandArgsConfig._get_fields(
            e, "name", "old_phone", "new_phone"
        ),
        "remove_phone": lambda e: CommandArgsConfig._get_fields(e, "name", "phone"),
        "edit_email": lambda e: CommandArgsConfig._get_fields(e, "name", "email"),
        "edit_address": lambda e: CommandArgsConfig._get_fields(e, "name", "address"),
        "delete_contact": lambda e: CommandArgsConfig._get_fields(e, "name"),
        "search_contacts": lambda e: CommandArgsConfig._get_first(
            e, "name", "phone", "email"
        ),
        "add_birthday": lambda e: CommandArgsConfig._get_fields(e, "name", "birthday"),
        "remove_birthday": lambda e: CommandArgsConfig._get_fields(e, "name"),
        "list_birthdays": lambda e: CommandArgsConfig._with_default(e, "days", "7"),
        "add_note": lambda e: CommandArgsConfig._get_fields(e, "note_text"),
        "edit_note": lambda e: CommandArgsConfig._get_fields(e, "id", "note_text"),
        "remove_note": lambda e: CommandArgsConfig._get_fields(e, "id"),
        "delete_note": lambda e: CommandArgsConfig._get_fields(e, "id"),
        "show_note": lambda e: CommandArgsConfig._get_fields(e, "id"),
        "add_note_tag": lambda e: CommandArgsConfig._get_fields(e, "id", "tag"),
        "remove_note_tag": lambda e: CommandArgsConfig._get_fields(e, "id", "tag"),
        "search_notes_text": lambda e: CommandArgsConfig._get_fields(e, "note_text"),
        "search_notes_by_tag": lambda e: CommandArgsConfig._get_fields(e, "tag"),
        "add_email": lambda e: CommandArgsConfig._get_fields(e, "name", "email"),
        "remove_email": lambda e: CommandArgsConfig._get_fields(e, "name"),
        "add_address": lambda e: CommandArgsConfig._get_fields(e, "name", "address"),
        "remove_address": lambda e: CommandArgsConfig._get_fields(e, "name"),
        "show_phone": lambda e: CommandArgsConfig._get_fields(e, "name"),
        "show_birthday": lambda e: CommandArgsConfig._get_fields(e, "name"),
    }

    SKIP_PIPELINE_INTENTS = ["list_birthdays"]
