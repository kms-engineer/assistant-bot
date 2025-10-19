import pytest
from src.domain.value_objects.tag import Tag

@pytest.mark.parametrize("valid_tag", [
    "python",
    "pytest-testing",
    "web-development",
    "a" * 50,
])
def test_tag_creation_with_valid_tag(valid_tag):
    """Tests that a Tag object is created successfully with a valid tag."""
    tag_obj = Tag(valid_tag)
    assert tag_obj.value == valid_tag

def test_tag_creation_strips_whitespace():
    """Tests that leading/trailing whitespace is stripped from a valid tag."""
    tag_with_spaces = "  padded-tag  "
    tag_obj = Tag(tag_with_spaces)
    assert tag_obj.value == "padded-tag"

@pytest.mark.parametrize("invalid_input, expected_error_message", [
    # Type and presence checks
    (None, "Tag must be a string"),
    (123, "Tag must be a string"),
    ([], "Tag must be a string"),
    ("", "Tag cannot be empty"),
    ("   ", "Tag cannot be empty"),

    # Length check
    ("a" * 51, "Tag too long (max 50 characters)"),
])
def test_tag_creation_with_invalid_input(invalid_input, expected_error_message):
    """
    Tests that creating a Tag with various invalid inputs raises a ValueError
    with the correct error message from the validator.
    """
    with pytest.raises(ValueError) as excinfo:
        Tag(invalid_input)
    assert str(excinfo.value) == expected_error_message
