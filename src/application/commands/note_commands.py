from typing import List
from ..services.note_service import NoteService
from ...domain.value_objects.tag import Tag
from ...domain.utils.styles_utils import stylize_tag

def add_note(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Add-note command requires text argument")

    text = " ".join(args)
    note_id = service.add_note(text)
    return f"Note added with ID: {note_id}"

def show_notes(args: List[str], service: NoteService) -> str:
    # Check if --sort-by-tag flag is present
    sort_by_tag = "--sort-by-tag" in args

    if sort_by_tag:
        # Get notes grouped by tags
        tag_groups = service.get_notes_sorted_by_tag()

        if not tag_groups:
            return "No notes found."

        lines = ["Notes grouped by tags:"]
        for tag_name, notes in tag_groups.items():
            lines.append(f"\n{stylize_tag(f'[{tag_name}]')} ({len(notes)} notes):")
            for note in notes:
                lines.append(f"  ID: {note.id}")
                lines.append(f"  Text: {note.text}")
                if note.tags and tag_name != "untagged":
                    all_tags = ", ".join(stylize_tag(str(tag)) for tag in note.tags)
                    lines.append(f"  Tags: {all_tags}")
                lines.append("")
    else:
        # Regular listing with tag highlighting
        notes = service.get_all_notes()

        if not notes:
            return "No notes found."

        lines = ["All notes:"]
        for note in notes:
            lines.append(f"ID: {note.id}")
            lines.append(f"Text: {note.text}")
            if note.tags:
                tags_str = ", ".join(stylize_tag(str(tag)) for tag in note.tags)
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
    """Add a tag to a note."""
    if len(args) < 2:
        raise ValueError("Add-tag command requires 2 arguments: note ID and tag")

    note_id = args[0]
    tag = " ".join(args[1:])
    return service.add_tag(note_id, tag)

def remove_tag(args: List[str], service: NoteService) -> str:
    """Remove a tag from a note."""
    if len(args) < 2:
        raise ValueError("Remove-tag command requires 2 arguments: note ID and tag")

    note_id = args[0]
    tag = " ".join(args[1:])
    return service.remove_tag(note_id, tag)

def search_notes(args: List[str], service: NoteService) -> str:
    """Search notes by text content."""
    if not args:
        raise ValueError("Search-notes command requires a search query")

    query = " ".join(args)
    notes = service.search_notes(query)

    if not notes:
        return f"No notes found matching '{query}'."

    lines = [f"Found {len(notes)} note(s) matching '{query}':"]
    for note in notes:
        lines.append(f"ID: {note.id}")
        lines.append(f"Text: {note.text}")
        if note.tags:
            tags_str = ", ".join(stylize_tag(str(tag)) for tag in note.tags)
            lines.append(f"Tags: {tags_str}")
        lines.append("")

    return "\n".join(lines)

def search_notes_by_tag(args: List[str], service: NoteService) -> str:
    """Search notes by tag."""
    if not args:
        raise ValueError("Search-notes-by-tag command requires a tag")

    tag = " ".join(args)
    notes = service.search_by_tag(tag)

    if not notes:
        return f"No notes found with tag '{tag}'."

    lines = [f"Found {len(notes)} note(s) with tag {stylize_tag(tag)}:"]
    for note in notes:
        lines.append(f"ID: {note.id}")
        lines.append(f"Text: {note.text}")
        if note.tags:
            tags_str = ", ".join(stylize_tag(str(tag)) for tag in note.tags)
            lines.append(f"Tags: {tags_str}")
        lines.append("")

    return "\n".join(lines)

def list_tags(args: List[str], service: NoteService) -> str:
    """List all unique tags with their usage count."""
    tag_counts = service.list_tags()

    if not tag_counts:
        return "No tags found."

    lines = [f"All tags ({len(tag_counts)} unique):"]
    for tag, count in tag_counts.items():
        lines.append(f"  {stylize_tag(tag)}: {count} note(s)")

    return "\n".join(lines)
