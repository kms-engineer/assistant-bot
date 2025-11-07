from src.domain.entities.note import Note
from src.domain.mappers.note_mapper import NoteMapper
from src.domain.models.dbnote import DBNote
from src.domain.value_objects.tag import Tag

test_title = "Test note title"

class TestNoteMapper:
    """Tests for the NoteMapper class."""

    def test_to_dbmodel_full(self):
        """Test mapping a full Note entity to a DBNote model."""
        note = Note(test_title, "Test note text", note_id="test-id-1")
        note.add_tag(Tag("tag1"))
        note.add_tag(Tag("tag2"))

        db_note = NoteMapper.to_dbmodel(note)

        assert isinstance(db_note, DBNote)
        assert db_note.id == "test-id-1"
        assert db_note.text == "Test note text"
        assert db_note.tags == "tag1,tag2"

    def test_to_dbmodel_no_tags(self):
        """Test mapping a Note entity with no tags to a DBNote model."""
        note = Note(test_title, "Another note", note_id="test-id-2")

        db_note = NoteMapper.to_dbmodel(note)

        assert isinstance(db_note, DBNote)
        assert db_note.id == "test-id-2"
        assert db_note.text == "Another note"
        assert db_note.tags is None

    def test_from_dbmodel_full(self):
        """Test mapping a full DBNote model to a Note entity."""
        db_note = DBNote(
            id="test-id-1",
            title=test_title,
            text="Test note text",
            tags="tag1, tag2, tag3"
        )

        note = NoteMapper.from_dbmodel(db_note)

        assert isinstance(note, Note)
        assert note.id == "test-id-1"
        assert note.text == "Test note text"
        assert len(note.tags) == 3
        assert Tag("tag1") in note.tags
        assert Tag("tag2") in note.tags
        assert Tag("tag3") in note.tags

    def test_from_dbmodel_no_tags(self):
        """Test mapping a DBNote model with no tags to a Note entity."""
        db_note = DBNote(
            id="test-id-2",
            title=test_title,
            text="Another note",
            tags=None
        )

        note = NoteMapper.from_dbmodel(db_note)

        assert isinstance(note, Note)
        assert note.id == "test-id-2"
        assert note.text == "Another note"
        assert len(note.tags) == 0
