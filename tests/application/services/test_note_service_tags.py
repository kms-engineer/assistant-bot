import pytest
from unittest.mock import Mock
from src.application.services.note_service import NoteService
from src.domain.entities.note import Note
from src.domain.value_objects import Tag

test_title = "Test note title"


@pytest.fixture
def mock_storage():
    """Create a mock storage for testing."""
    storage = Mock()
    storage.storage_type = Mock()
    storage.storage_type.name = "JSON"
    return storage


@pytest.fixture
def note_service(mock_storage):
    """Create a NoteService with mock storage."""
    service = NoteService(storage=mock_storage)
    return service


@pytest.fixture
def sample_notes(note_service):
    """Create sample notes for testing."""
    # Add notes with tags
    id1 = note_service.add_note("Note title1", "Python programming basics")
    note_service.add_tag(id1, Tag("python"))
    note_service.add_tag(id1, Tag("programming"))

    id2 = note_service.add_note("Note title2", "JavaScript async patterns")
    note_service.add_tag(id2, Tag("javascript"))
    note_service.add_tag(id2, Tag("async"))

    id3 = note_service.add_note("Note title3", "Python testing with pytest")
    note_service.add_tag(id3, Tag("python"))
    note_service.add_tag(id3, Tag("testing"))
    id4 = note_service.add_note("Note title4", "Untagged note")

    return {"ids": [id1, id2, id3, id4], "service": note_service}


class TestAddTag:
    """Tests for NoteService.add_tag method."""

    def test_add_tag_success(self, note_service):
        """Test adding a tag to a note."""
        note_id = note_service.add_note(test_title, "Test note")
        result = note_service.add_tag(note_id, Tag("test-tag"))

        assert result == "Tag added."
        note = note_service.notes[note_id]
        assert len(note.tags) == 1
        assert note.tags[0] == Tag("test-tag")

    def test_add_tag_with_trim(self, note_service):
        """Test that tags are trimmed before adding."""
        note_id = note_service.add_note(test_title, "Test note")
        note_service.add_tag(note_id, Tag("  spaced  "))

        note = note_service.notes[note_id]
        assert note.tags[0] == Tag("spaced")

    def test_add_tag_duplicate_raises_error(self, note_service):
        """Test that adding duplicate tag raises error."""
        note_id = note_service.add_note(test_title, "Test note")
        note_service.add_tag(note_id, Tag("duplicate"))

        with pytest.raises(ValueError, match="Tag already exists"):
            note_service.add_tag(note_id, Tag("duplicate"))

    def test_add_tag_duplicate_case_insensitive(self, note_service):
        """Test that duplicate detection is case-sensitive (tags preserve case)."""
        note_id = note_service.add_note(test_title, "Test note")
        note_service.add_tag(note_id, Tag("Python"))

        # Case-sensitive duplicate should raise error (same tag)
        with pytest.raises(ValueError, match="Tag already exists"):
            note_service.add_tag(note_id, Tag("Python"))

    def test_add_tag_note_not_found(self, note_service):
        """Test that adding tag to non-existent note raises error."""
        with pytest.raises(KeyError, match="Note not found"):
            note_service.add_tag("nonexistent-id", Tag("tag"))

    def test_add_tag_empty_raises_error(self, note_service):
        """Test that empty tag raises error."""
        note_id = note_service.add_note(test_title, "Test note")

        with pytest.raises(ValueError):
            note_service.add_tag(note_id, Tag(""))

    def test_add_tag_too_long_raises_error(self, note_service):
        """Test that tag longer than 50 chars raises error."""
        note_id = note_service.add_note(test_title, "Test note")
        long_tag = "a" * 51

        with pytest.raises(ValueError, match="Tag too long"):
            note_service.add_tag(note_id, Tag(long_tag))

    def test_add_multiple_tags(self, note_service):
        """Test adding multiple tags to a note."""
        note_id = note_service.add_note(test_title, "Test note")
        note_service.add_tag(note_id, Tag("tag1"))
        note_service.add_tag(note_id, Tag("tag2"))
        note_service.add_tag(note_id, Tag("tag3"))

        note = note_service.notes[note_id]
        assert len(note.tags) == 3
        tag_values = [tag.value for tag in note.tags]
        assert "tag1" in tag_values
        assert "tag2" in tag_values
        assert "tag3" in tag_values


class TestRemoveTag:
    """Tests for NoteService.remove_tag method."""

    def test_remove_tag_success(self, note_service):
        """Test removing a tag from a note."""
        note_id = note_service.add_note(test_title, "Test note")
        note_service.add_tag(note_id, Tag("remove-me"))
        result = note_service.remove_tag(note_id, Tag("remove-me"))

        assert result == "Tag removed."
        note = note_service.notes[note_id]
        assert len(note.tags) == 0

    def test_remove_tag_not_found(self, note_service):
        """Test that removing non-existent tag raises error."""
        note_id = note_service.add_note(test_title, "Test note")

        with pytest.raises(ValueError, match="Tag not found"):
            note_service.remove_tag(note_id, Tag("nonexistent"))

    def test_remove_tag_note_not_found(self, note_service):
        """Test that removing tag from non-existent note raises error."""
        with pytest.raises(KeyError, match="Note not found"):
            note_service.remove_tag("nonexistent-id", Tag("tag"))

    def test_remove_one_of_many_tags(self, note_service):
        """Test removing one tag when note has multiple tags."""
        note_id = note_service.add_note(test_title, "Test note")
        note_service.add_tag(note_id, Tag("tag1"))
        note_service.add_tag(note_id, Tag("tag2"))
        note_service.add_tag(note_id, Tag("tag3"))

        note_service.remove_tag(note_id, Tag("tag2"))

        note = note_service.notes[note_id]
        assert len(note.tags) == 2

        assert Tag("tag1") in note.tags
        assert Tag("tag3") in note.tags
        assert Tag("tag2") not in note.tags


class TestSearchByTag:
    """Tests for NoteService.search_by_tag method."""

    def test_search_by_tag_finds_notes(self, sample_notes):
        """Test searching notes by tag."""
        service = sample_notes["service"]
        results = service.search_notes_by_tag("python")

        assert len(results) == 2
        texts = [note.text for note in results]
        assert "Python programming basics" in texts
        assert "Python testing with pytest" in texts

    def test_search_by_tag_case_insensitive(self, sample_notes):
        """Test that tag search is case-insensitive."""
        service = sample_notes["service"]
        results_lower = service.search_notes_by_tag("python")
        results_upper = service.search_notes_by_tag("PYTHON")
        results_mixed = service.search_notes_by_tag("PyThOn")

        assert len(results_lower) == len(results_upper) == len(results_mixed) == 2

    def test_search_by_tag_no_results(self, sample_notes):
        """Test searching by non-existent tag."""
        service = sample_notes["service"]
        results = service.search_notes_by_tag("nonexistent")

        assert len(results) == 0

    def test_search_by_tag_unique_tag(self, sample_notes):
        """Test searching by tag that only one note has."""
        service = sample_notes["service"]
        results = service.search_notes_by_tag("javascript")

        assert len(results) == 1
        assert results[0].text == "JavaScript async patterns"


class TestListTags:
    """Tests for NoteService.list_tags method."""

    def test_list_tags_with_counts(self, sample_notes):
        """Test listing all tags with counts."""
        service = sample_notes["service"]
        tag_counts = service.list_tags()

        assert len(tag_counts) == 5
        assert tag_counts["python"] == 2
        assert tag_counts["programming"] == 1
        assert tag_counts["javascript"] == 1
        assert tag_counts["async"] == 1
        assert tag_counts["testing"] == 1

    def test_list_tags_empty(self, note_service):
        """Test listing tags when no notes exist."""
        tag_counts = note_service.list_tags()

        assert len(tag_counts) == 0
        assert tag_counts == {}

    def test_list_tags_sorted_alphabetically(self, sample_notes):
        """Test that tags are sorted alphabetically."""
        service = sample_notes["service"]
        tag_counts = service.list_tags()

        tag_names = list(tag_counts.keys())
        assert tag_names == sorted(tag_names)

    def test_list_tags_excludes_untagged_notes(self, sample_notes):
        """Test that untagged notes don't affect tag list."""
        service = sample_notes["service"]
        tag_counts = service.list_tags()

        # Should only have tags from tagged notes
        assert "untagged" not in tag_counts
        assert len(tag_counts) == 5  # Only actual tags


class TestGetNotesSortedByTag:
    """Tests for NoteService.get_notes_sorted_by_tag method."""

    def test_get_notes_sorted_by_tag(self, sample_notes):
        """Test grouping notes by tags."""
        service = sample_notes["service"]
        tag_groups = service.get_notes_sorted_by_tag()

        assert "python" in tag_groups
        assert len(tag_groups["python"]) == 2

        assert "javascript" in tag_groups
        assert len(tag_groups["javascript"]) == 1

        assert "untagged" in tag_groups
        assert len(tag_groups["untagged"]) == 1

    def test_get_notes_sorted_by_tag_sorted_keys(self, sample_notes):
        """Test that tag groups are sorted by tag name."""
        service = sample_notes["service"]
        tag_groups = service.get_notes_sorted_by_tag()

        tag_names = list(tag_groups.keys())
        assert tag_names == sorted(tag_names)

    def test_get_notes_sorted_by_tag_note_in_multiple_groups(self, sample_notes):
        """Test that notes with multiple tags appear in multiple groups."""
        service = sample_notes["service"]
        tag_groups = service.get_notes_sorted_by_tag()

        # First note has both "python" and "programming" tags
        python_notes = tag_groups["python"]
        programming_notes = tag_groups["programming"]

        # Check that the first note appears in both groups
        python_texts = [note.text for note in python_notes]
        programming_texts = [note.text for note in programming_notes]

        assert "Python programming basics" in python_texts
        assert "Python programming basics" in programming_texts

    def test_get_notes_sorted_by_tag_empty(self, note_service):
        """Test grouping when no notes exist."""
        tag_groups = note_service.get_notes_sorted_by_tag()

        assert len(tag_groups) == 0
        assert tag_groups == {}

    def test_get_notes_sorted_by_tag_only_untagged(self, note_service):
        """Test grouping when only untagged notes exist."""
        note_service.add_note(test_title, "Untagged 1")
        note_service.add_note(test_title, "Untagged 2")

        tag_groups = note_service.get_notes_sorted_by_tag()

        assert len(tag_groups) == 1
        assert "untagged" in tag_groups
        assert len(tag_groups["untagged"]) == 2


class TestSearchNotes:
    """Tests for NoteService.search_notes method (text search)."""

    def test_search_notes_finds_matches(self, sample_notes):
        """Test text search finds matching notes."""
        service = sample_notes["service"]
        results = service.search_notes_by_content("Python")

        assert len(results) == 2
        texts = [note.text for note in results]
        assert "Python programming basics" in texts
        assert "Python testing with pytest" in texts

    def test_search_notes_case_insensitive(self, sample_notes):
        """Test that text search is case-insensitive."""
        service = sample_notes["service"]
        results_lower = service.search_notes_by_content("python")
        results_upper = service.search_notes_by_content("PYTHON")

        assert len(results_lower) == len(results_upper) == 2

    def test_search_notes_partial_match(self, sample_notes):
        """Test that search matches partial text."""
        service = sample_notes["service"]
        results = service.search_notes_by_content("async")

        assert len(results) == 1
        assert "JavaScript async patterns" in results[0].text

    def test_search_notes_no_results(self, sample_notes):
        """Test searching with no matches."""
        service = sample_notes["service"]
        results = service.search_notes_by_content("nonexistent query")

        assert len(results) == 0
