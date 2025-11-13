from typing import List

from colorama import Style

from ..services.note_service import NoteService
from ...domain.entities import Note
from ...domain.utils.styles_utils import stylize_tag
from ...domain.value_objects.tag import Tag
from ...presentation.cli.confirmation import confirm_action
from ...presentation.cli.ui_messages import UIMessages


def add_note(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Add-note command requires text argument")

    # If only one argument provided, use it as both title and text
    if len(args) == 1:
        title = args[0]
        text = args[0]
    else:
        # Multiple arguments: first is title, rest is text
        title = args[0]
        text = " ".join(args[1:])

    note_id = service.add_note(title, text)
    return f"Note added with ID: {note_id}"


def append_notes(lines: List[str], notes: List[Note]):
    for note in notes:
        lines.append(f"ID: {note.id}")
        lines.append(f"Title: {note.title}")
        lines.append(f"Text: {note.text}")
        if note.tags:
            tags_str = ", ".join(stylize_tag(str(tag)) for tag in note.tags)
            lines.append(f"Tags: {tags_str}")
        lines.append("")


def show_notes(args: List[str], service: NoteService) -> str:
    # Check if --sort-by-tag flag is present
    sort_by_tag = "--sort-by-tag" in args
    sort_by_title = "--sort-by-title" in args

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
                lines.append(f"  Title: {note.title}")
                lines.append(f"  Text: {note.text}")
                if note.tags and tag_name != "untagged":
                    all_tags = ", ".join(stylize_tag(str(tag)) for tag in note.tags)
                    lines.append(f"  Tags: {all_tags}")
                lines.append("")
    else:
        # Regular listing with tag highlighting
        notes = (
            service.get_notes_sorted_by_title()
            if sort_by_title
            else service.get_all_notes()
        )

        if not notes:
            return "No notes found."

        lines = [f"All notes:{Style.RESET_ALL}"]
        append_notes(lines, notes)

    return "\n".join(lines)


def show_note(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Show-note command requires note ID argument")

    note_id = args[0]
    note = service.get_note_by_id(note_id)

    if not note:
        return f"Note not found with ID: {note_id}"

    lines = [f"Note ID: {note.id}"]
    lines.append(f"Text: {note.text}")
    if note.tags:
        tags_str = ", ".join(stylize_tag(str(tag)) for tag in note.tags)
        lines.append(f"Tags: {tags_str}")

    return "\n".join(lines)


def edit_note(args: List[str], service: NoteService) -> str:
    if len(args) < 2:
        raise ValueError("Edit-note command requires 2 arguments: ID and new text")

    note_id = args[0]
    new_text = " ".join(args[1:])

    # Get current note to show in confirmation
    note = service.get_note_by_id(note_id)
    if not note:
        return f"Note not found with ID: {note_id}"

    # Ask for confirmation
    prompt = (
        f"Edit note '{note.id}'? Old text: '{note.text[:50]}...'"
        if len(note.text) > 50
        else f"Edit note '{note.id}'? Old text: '{note.text}'"
    )
    if not confirm_action(prompt, default=True):
        return UIMessages.ACTION_CANCELLED

    return service.edit_note(note_id, new_text)


def delete_note(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Delete-note command requires ID argument")

    note_id = args[0]
    note = service.get_note_by_id(note_id)
    if not note:
        return f"Note not found with ID: {note_id}"

    # Ask for confirmation
    text_preview = note.text[:50] + "..." if len(note.text) > 50 else note.text
    prompt = f"Delete note '{note_id}'? Text: '{text_preview}'. This can't be undone"
    if not confirm_action(prompt, default=False):
        return UIMessages.ACTION_CANCELLED

    return service.delete_note_by_id(note_id)


def add_tag(args: List[str], service: NoteService) -> str:
    if len(args) < 2:
        raise ValueError("Add-tag command requires 2 arguments: note ID and tag")
    note_id = args[0]
    tag = Tag(args[1])
    return service.add_tag(note_id, tag)


def remove_tag(args: List[str], service: NoteService) -> str:
    if len(args) < 2:
        raise ValueError("Remove-tag command requires 2 arguments: note ID and tag")

    note_id = args[0]
    tag = Tag(args[1])

    # Ask for confirmation
    prompt = f"Remove tag '{tag.value}' from note '{note_id}'?"
    if not confirm_action(prompt, default=False):
        return UIMessages.ACTION_CANCELLED

    return service.remove_tag(note_id, tag)


def search_notes(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Search-notes command requires a search query")

    query = " ".join(args)
    # Call the service method expected by tests/mocks
    notes = service.search_notes(query)

    if not notes:
        return f"No notes found matching '{query}'"

    lines = [f"Found {len(notes)} note(s) matching '{query}'{Style.RESET_ALL}"]
    append_notes(lines, notes)

    return "\n".join(lines)


def search_notes_by_tag(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Search-notes-by-tag command requires a tag")

    tag = " ".join(args)
    # Tests expect the service method name "search_by_tag"
    notes = service.search_by_tag(tag)

    if not notes:
        return f"No notes found with tag '{tag}'"

    lines = [f"Found {len(notes)} note(s) with tag {stylize_tag(tag)}"]
    append_notes(lines, notes)

    return "\n".join(lines)


def delete_note_by_title(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Delete-note-by-title command requires a title")
    title = " ".join(args)
    return service.delete_note_by_title(title)


def delete_note_by_tag(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Delete-note-by-tag command requires a tag")
    tag = " ".join(args)
    return service.delete_note_by_tags(tag)


def rename_note(args: List[str], service: NoteService) -> str:
    if len(args) < 2:
        raise ValueError("Rename-note command requires 2 arguments: ID and new title")
    note_id = args[0]
    new_title = " ".join(args[1:])
    return service.rename_note(note_id, new_title)


def get_note_ids(service: NoteService) -> str:
    ids = service.get_ids()
    if not ids:
        return "No notes loaded."
    return ", ".join(sorted(ids))


def get_titles(service: NoteService) -> str:
    titles = service.get_titles()
    if not titles:
        return "No notes loaded."
    return "\n".join(sorted(titles))


def save_notes(args: List[str], service: NoteService) -> str:
    filename = None
    if args:
        filename = args[0]
    return service.save_notes(filename)


def load_notes(args: List[str], service: NoteService) -> str:
    filename = None
    if args:
        filename = args[0]
    count = service.load_notes(filename)
    return f"Loaded {count} notes."


def get_notes_current_filename(service: NoteService) -> str:
    return service.get_current_filename()


def get_all_notes(service: NoteService) -> str:
    notes = service.get_all_notes()
    if not notes:
        return "No notes found."
    lines: List[str] = []
    append_notes(lines, notes)
    return "\n".join(lines)


def search_notes_by_title(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Search-notes-by-title requires a title")
    title = " ".join(args)
    notes = service.search_notes_by_title(title)
    if not notes:
        return f"No notes found with title '{title}'."
    lines: List[str] = [f"Found {len(notes)} note(s) with title '{title}':"]
    append_notes(lines, notes)
    return "\n".join(lines)


def get_note_by_title(args: List[str], service: NoteService) -> str:
    if not args:
        raise ValueError("Get-note-by-title requires a title")
    title = " ".join(args)
    note = service.get_note_id_by_title(title)
    if not note:
        return f"No note found with title '{title}'."
    lines: List[str] = []
    append_notes(lines, [note])
    return "\n".join(lines)


def list_tags(service: NoteService) -> str:
    tag_counts = service.list_tags()

    if not tag_counts:
        return "No tags found."

    lines = [f"All tags ({len(tag_counts)} unique):"]
    for tag, count in tag_counts.items():
        lines.append(f"  {stylize_tag(tag)}: {count} note(s)")

    return "\n".join(lines)
