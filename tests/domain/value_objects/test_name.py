import pytest
from src.domain.value_objects.name import Name

def test_name_creation_with_valid_name():
    """Tests that a Name object is created successfully with a valid name."""
    name_obj = Name("John Doe")
    assert name_obj.value == "John Doe"

def test_name_creation_strips_whitespace():
    """Tests that leading/trailing whitespace is stripped from a valid name."""
    name_with_spaces = "  Jane Smith  "
    name_obj = Name(name_with_spaces)
    assert name_obj.value == "Jane Smith"

@pytest.mark.parametrize("invalid_input", [
    "",
    "   ",
])
def test_name_creation_with_empty_or_whitespace_name(invalid_input):
    """
    Tests that creating a Name with an empty or whitespace string raises a ValueError.
    """
    with pytest.raises(ValueError) as excinfo:
        Name(invalid_input)
    assert str(excinfo.value) == "Name cannot be empty or whitespace."

@pytest.mark.parametrize("non_string_input", [
    123,
])
def test_name_creation_with_non_string_input(non_string_input):
    """
    Tests that creating a Name with a non-string input raises an AttributeError
    because the `.strip()` method is called on a non-string type.
    """
    with pytest.raises(AttributeError):
        Name(non_string_input)

@pytest.mark.parametrize("non_string_input", [
    None,
    [],
])
def test_name_creation_with_non_string_input(non_string_input):
    """
    Tests that creating a Name with a non-string input raises an ValueError
    """
    with pytest.raises(ValueError):
        Name(non_string_input)
