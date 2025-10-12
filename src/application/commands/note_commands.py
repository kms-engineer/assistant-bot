from typing import List
from ..services.note_service import NoteService

def add_note(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Add-note command requires text argument")

    text = " ".join(args)
    note_id = service.add_note(text)
    return f"Note added with ID: {note_id}"

def show_notes(args: List[str], service: NoteService) -> str:
    notes = service.get_all_notes()

    if not notes:
        return "No notes found."

    lines = ["All notes:"]
    for note in notes:
        lines.append(f"ID: {note.id}")
        lines.append(f"Text: {note.text}")
        if note.tags:
            tags_str = ", ".join(str(tag) for tag in note.tags)
            lines.append(f"Tags: {tags_str}")
        lines.append("")

    return "\n".join(lines)

def edit_note(args: List[str], service: NoteService) -> str:
    if len(args) < 2:
        raise ValueError("Edit-note command requires 2 arguments: ID and new text")

    note_id = args[0]
    new_text = " ".join(args[1:])

    return service.edit_note(note_id, new_text)

def delete_note(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Delete-note command requires ID argument")

    note_id = args[0]  # ID нотатки
    return service.delete_note(note_id)
