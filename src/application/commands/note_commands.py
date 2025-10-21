from typing import List
from ..services.note_service import NoteService
from ...domain.value_objects.tag import Tag

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

    note_id = args[0]
    return service.delete_note(note_id)

def add_tag(args: List[str], service: NoteService) -> str:
    if len(args) < 2:
        raise ValueError("Add-tag command requires 2 arguments: note ID and tag")

    note_id = args[0]
    tag_vo = Tag(args[1])
    return service.add_tag(note_id, tag_vo)

def remove_tag(args: List[str], service: NoteService) -> str:
    if len(args) < 2:
        raise ValueError("Remove-tag command requires 2 arguments: note ID and tag")

    note_id = args[0]
    tag_vo = Tag(args[1])
    return service.remove_tag(note_id, tag_vo)

def search_notes(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Search-notes command requires search query argument")

    query = " ".join(args)
    notes = service.search_notes(query)

    if not notes:
        return f"No notes found matching: {query}"

    lines = [f"Notes matching '{query}':"]
    for note in notes:
        lines.append(f"ID: {note.id}")
        lines.append(f"Text: {note.text}")
        if note.tags:
            tags_str = ", ".join(str(tag) for tag in note.tags)
            lines.append(f"Tags: {tags_str}")
        lines.append("")

    return "\n".join(lines)

def search_by_tag(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Search-by-tag command requires tag argument")

    tag = args[0]
    notes = service.search_by_tag(tag)

    if not notes:
        return f"No notes found with tag: {tag}"

    lines = [f"Notes with tag '{tag}':"]
    for note in notes:
        lines.append(f"ID: {note.id}")
        lines.append(f"Text: {note.text}")
        if note.tags:
            tags_str = ", ".join(str(tag) for tag in note.tags)
            lines.append(f"Tags: {tags_str}")
        lines.append("")

    return "\n".join(lines)
