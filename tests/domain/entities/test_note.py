import pytest
from unittest.mock import Mock
from src.domain.entities.note import Note
from src.domain.value_objects.tag import Tag


class TestNote:
    """Tests for the Note entity."""

    def test_note_creation_success(self):
        """Test successful creation of a Note."""
        note = Note("  Test note text  ", "test-id-1")
        assert note.text == "Test note text"
        assert note.id == "test-id-1"
        assert note.tags == []

    def test_note_creation_empty_text_raises_error(self):
        """Test that creating a note with empty text raises ValueError."""
        with pytest.raises(ValueError, match="Note text cannot be empty"):
            Note("", "test-id-1")
        with pytest.raises(ValueError, match="Note text cannot be empty"):
            Note("   ", "test-id-1")

    def test_note_creation_empty_id_raises_error(self):
        """Test that creating a note with an empty ID raises ValueError."""
        with pytest.raises(ValueError, match="Note ID is required"):
            Note("Some text", "")

    def test_create_classmethod(self):
        """Test the create classmethod for generating a note with a new ID."""
        id_generator = Mock(return_value="new-unique-id")
        note = Note.create("New note from classmethod", id_generator)
        assert isinstance(note, Note)
        assert note.id == "new-unique-id"
        assert note.text == "New note from classmethod"
        id_generator.assert_called_once()

    def test_add_tag_success(self):
        """Test adding a new tag to a note."""
        note = Note("Test note", "id-1")
        tag = Tag("python")
        note.add_tag(tag)
        assert len(note.tags) == 1
        assert tag in note.tags

    def test_add_duplicate_tag_raises_error(self):
        """Test that adding a duplicate tag raises ValueError."""
        note = Note("Test note", "id-1")
        tag = Tag("python")
        note.add_tag(tag)
        with pytest.raises(ValueError, match="Tag already exists"):
            note.add_tag(tag)

    def test_remove_tag_success(self):
        """Test removing an existing tag from a note."""
        note = Note("Test note", "id-1")
        tag = Tag("python")
        note.add_tag(tag)
        note.remove_tag(tag)
        assert len(note.tags) == 0

    def test_remove_nonexistent_tag_raises_error(self):
        """Test that removing a non-existent tag raises ValueError."""
        note = Note("Test note", "id-1")
        tag = Tag("python")
        with pytest.raises(ValueError, match="Tag not found"):
            note.remove_tag(tag)

    def test_edit_text_success(self):
        """Test successfully editing the text of a note."""
        note = Note("Initial text", "id-1")
        note.edit_text("  Updated text  ")
        assert note.text == "Updated text"

    def test_edit_text_empty_raises_error(self):
        """Test that editing text to an empty string raises ValueError."""
        note = Note("Initial text", "id-1")
        with pytest.raises(ValueError, match="Note text cannot be empty"):
            note.edit_text("")
        with pytest.raises(ValueError, match="Note text cannot be empty"):
            note.edit_text("   ")

    def test_str_representation_with_tags_and_long_text(self):
        """Test the string representation of a note with tags and long text."""
        note = Note("This is a very long note text that should be truncated.", "id-1")
        note.add_tag(Tag("long"))
        note.add_tag(Tag("test"))
        expected = "Note [long, test]: This is a very long note text that should be trunc..."
        assert str(note) == expected

    def test_str_representation_no_tags_short_text(self):
        """Test the string representation of a note with no tags and short text."""
        note = Note("Short note.", "id-2")
        expected = "Note [no tags]: Short note."
        assert str(note) == expected
