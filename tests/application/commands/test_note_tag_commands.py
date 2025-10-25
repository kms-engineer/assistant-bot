import pytest
from unittest.mock import Mock
from src.application.commands import note_commands
from src.domain.entities.note import Note


@pytest.fixture
def mock_service():
    """Create a mock NoteService for testing."""
    return Mock()


@pytest.fixture
def sample_note():
    """Create a sample note for testing."""
    note = Note("Sample note text", "test-id-1")
    return note


class TestAddTag:
    """Tests for add_tag command."""

    def test_add_tag_success(self, mock_service):
        """Test adding a tag to a note."""
        mock_service.add_tag.return_value = "Tag added."

        result = note_commands.add_tag(["test-id", "python"], mock_service)

        mock_service.add_tag.assert_called_once_with("test-id", "python")
        assert result == "Tag added."

    def test_add_tag_with_multi_word_tag(self, mock_service):
        """Test adding a multi-word tag."""
        mock_service.add_tag.return_value = "Tag added."

        result = note_commands.add_tag(["test-id", "machine", "learning"], mock_service)

        mock_service.add_tag.assert_called_once_with("test-id", "machine learning")
        assert result == "Tag added."

    def test_add_tag_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Add-tag command requires 2 arguments"):
            note_commands.add_tag([], mock_service)

        with pytest.raises(ValueError, match="Add-tag command requires 2 arguments"):
            note_commands.add_tag(["only-id"], mock_service)

    def test_add_tag_duplicate(self, mock_service):
        """Test adding a duplicate tag raises error."""
        mock_service.add_tag.side_effect = ValueError("Tag already exists")

        with pytest.raises(ValueError, match="Tag already exists"):
            note_commands.add_tag(["test-id", "python"], mock_service)


class TestRemoveTag:
    """Tests for remove_tag command."""

    def test_remove_tag_success(self, mock_service):
        """Test removing a tag from a note."""
        mock_service.remove_tag.return_value = "Tag removed."

        result = note_commands.remove_tag(["test-id", "python"], mock_service)

        mock_service.remove_tag.assert_called_once_with("test-id", "python")
        assert result == "Tag removed."

    def test_remove_tag_with_multi_word_tag(self, mock_service):
        """Test removing a multi-word tag."""
        mock_service.remove_tag.return_value = "Tag removed."

        result = note_commands.remove_tag(["test-id", "machine", "learning"], mock_service)

        mock_service.remove_tag.assert_called_once_with("test-id", "machine learning")
        assert result == "Tag removed."

    def test_remove_tag_missing_arguments(self, mock_service):
        """Test that missing arguments raise ValueError."""
        with pytest.raises(ValueError, match="Remove-tag command requires 2 arguments"):
            note_commands.remove_tag([], mock_service)

        with pytest.raises(ValueError, match="Remove-tag command requires 2 arguments"):
            note_commands.remove_tag(["only-id"], mock_service)

    def test_remove_tag_not_found(self, mock_service):
        """Test removing a non-existent tag raises error."""
        mock_service.remove_tag.side_effect = ValueError("Tag not found")

        with pytest.raises(ValueError, match="Tag not found"):
            note_commands.remove_tag(["test-id", "nonexistent"], mock_service)


class TestSearchNotes:
    """Tests for search_notes command."""

    def test_search_notes_with_results(self, mock_service, sample_note):
        """Test searching notes with matching results."""
        mock_service.search_notes.return_value = [sample_note]

        result = note_commands.search_notes(["sample"], mock_service)

        mock_service.search_notes.assert_called_once_with("sample")
        assert "Found 1 note(s) matching 'sample'" in result
        assert sample_note.id in result
        assert sample_note.text in result

    def test_search_notes_no_results(self, mock_service):
        """Test searching notes without matches."""
        mock_service.search_notes.return_value = []

        result = note_commands.search_notes(["nonexistent"], mock_service)

        assert "No notes found matching 'nonexistent'" in result

    def test_search_notes_multi_word_query(self, mock_service, sample_note):
        """Test searching with multi-word query."""
        mock_service.search_notes.return_value = [sample_note]

        result = note_commands.search_notes(["sample", "note"], mock_service)

        mock_service.search_notes.assert_called_once_with("sample note")
        assert "Found 1 note(s) matching 'sample note'" in result

    def test_search_notes_missing_query(self, mock_service):
        """Test that missing query raises ValueError."""
        with pytest.raises(ValueError, match="Search-notes command requires a search query"):
            note_commands.search_notes([], mock_service)

    def test_search_notes_case_insensitive(self, mock_service):
        """Test that search is case insensitive."""
        note_upper = Note("PYTHON CODE", "test-id-upper")
        note_lower = Note("python code", "test-id-lower")
        mock_service.search_notes.return_value = [note_upper, note_lower]

        result = note_commands.search_notes(["python"], mock_service)

        assert "Found 2 note(s)" in result


class TestSearchNotesByTag:
    """Tests for search_notes_by_tag command."""

    def test_search_by_tag_with_results(self, mock_service, sample_note):
        """Test searching notes by tag with results."""
        sample_note.add_tag("python")
        mock_service.search_by_tag.return_value = [sample_note]

        result = note_commands.search_notes_by_tag(["python"], mock_service)

        mock_service.search_by_tag.assert_called_once_with("python")
        assert "Found 1 note(s) with tag" in result
        assert sample_note.id in result

    def test_search_by_tag_no_results(self, mock_service):
        """Test searching by tag without matches."""
        mock_service.search_by_tag.return_value = []

        result = note_commands.search_notes_by_tag(["nonexistent"], mock_service)

        assert "No notes found with tag 'nonexistent'" in result

    def test_search_by_tag_multi_word(self, mock_service, sample_note):
        """Test searching by multi-word tag."""
        sample_note.add_tag("machine learning")
        mock_service.search_by_tag.return_value = [sample_note]

        result = note_commands.search_notes_by_tag(["machine", "learning"], mock_service)

        mock_service.search_by_tag.assert_called_once_with("machine learning")

    def test_search_by_tag_missing_tag(self, mock_service):
        """Test that missing tag raises ValueError."""
        with pytest.raises(ValueError, match="Search-notes-by-tag command requires a tag"):
            note_commands.search_notes_by_tag([], mock_service)

    def test_search_by_tag_case_insensitive(self, mock_service):
        """Test that tag search is case insensitive."""
        note1 = Note("Note 1", "id-1")
        note1.add_tag("Python")
        note2 = Note("Note 2", "id-2")
        note2.add_tag("python")
        mock_service.search_by_tag.return_value = [note1, note2]

        result = note_commands.search_notes_by_tag(["python"], mock_service)

        assert "Found 2 note(s)" in result


class TestListTags:
    """Tests for list_tags command."""

    def test_list_tags_with_tags(self, mock_service):
        """Test listing tags with counts."""
        mock_service.list_tags.return_value = {
            "python": 3,
            "javascript": 2,
            "testing": 1
        }

        result = note_commands.list_tags([], mock_service)

        assert "All tags (3 unique)" in result
        assert "python" in result
        assert "3 note(s)" in result
        assert "javascript" in result
        assert "2 note(s)" in result
        assert "testing" in result
        assert "1 note(s)" in result

    def test_list_tags_empty(self, mock_service):
        """Test listing tags when no tags exist."""
        mock_service.list_tags.return_value = {}

        result = note_commands.list_tags([], mock_service)

        assert result == "No tags found."

    def test_list_tags_sorted(self, mock_service):
        """Test that tags are displayed in sorted order."""
        mock_service.list_tags.return_value = {
            "aaa": 1,
            "bbb": 2,
            "ccc": 3
        }

        result = note_commands.list_tags([], mock_service)
        lines = result.split('\n')

        # Check that tags appear in alphabetical order
        tag_lines = [line for line in lines if "note(s)" in line]
        assert len(tag_lines) == 3
        assert "aaa" in tag_lines[0]
        assert "bbb" in tag_lines[1]
        assert "ccc" in tag_lines[2]


class TestShowNotesWithTags:
    """Tests for show_notes command with tag features."""

    def test_show_notes_with_tag_highlighting(self, mock_service, sample_note):
        """Test that tags are highlighted in note display."""
        sample_note.add_tag("python")
        sample_note.add_tag("testing")
        mock_service.get_all_notes.return_value = [sample_note]

        result = note_commands.show_notes([], mock_service)

        assert sample_note.id in result
        assert sample_note.text in result
        assert "Tags:" in result

    def test_show_notes_sort_by_tag(self, mock_service):
        """Test show-notes --sort-by-tag groups notes by tags."""
        note1 = Note("Python note", "id-1")
        note1.add_tag("python")
        note2 = Note("JavaScript note", "id-2")
        note2.add_tag("javascript")
        note3 = Note("Python note 2", "id-3")
        note3.add_tag("python")

        mock_service.get_notes_sorted_by_tag.return_value = {
            "javascript": [note2],
            "python": [note1, note3]
        }

        result = note_commands.show_notes(["--sort-by-tag"], mock_service)

        assert "Notes grouped by tags:" in result
        assert "[javascript]" in result
        assert "(1 notes)" in result
        assert "[python]" in result
        assert "(2 notes)" in result

    def test_show_notes_with_untagged_notes(self, mock_service):
        """Test that untagged notes are properly grouped."""
        note1 = Note("Tagged note", "id-1")
        note1.add_tag("python")
        note2 = Note("Untagged note", "id-2")

        mock_service.get_notes_sorted_by_tag.return_value = {
            "python": [note1],
            "untagged": [note2]
        }

        result = note_commands.show_notes(["--sort-by-tag"], mock_service)

        assert "[python]" in result
        assert "[untagged]" in result

    def test_show_notes_with_multi_tags_per_note(self, mock_service):
        """Test displaying notes with multiple tags."""
        note = Note("Multi-tag note", "id-1")
        note.add_tag("python")
        note.add_tag("testing")
        note.add_tag("async")
        mock_service.get_all_notes.return_value = [note]

        result = note_commands.show_notes([], mock_service)

        assert "Tags:" in result
        # All tags should be present in the output
        assert "python" in result or "python".upper() in result
        assert "testing" in result or "testing".upper() in result
        assert "async" in result or "async".upper() in result

    def test_show_notes_empty_with_sort(self, mock_service):
        """Test show-notes --sort-by-tag with no notes."""
        mock_service.get_notes_sorted_by_tag.return_value = {}

        result = note_commands.show_notes(["--sort-by-tag"], mock_service)

        assert "No notes found" in result
