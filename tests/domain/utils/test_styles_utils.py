import pytest
from colorama import Fore, Style
from src.domain.utils.styles_utils import (
    stylize_text,
    stylize_error_message,
    stylize_success_message,
    stylize_warning_message,
    stylize_errors,
    stylize_success,
    stylize_warning,
    stylize_tag,
)


class TestStylingFunctions:
    """Tests for the styling utility functions."""

    def test_stylize_text(self):
        """Test the default text stylization."""
        message = "Hello, World!"
        expected = f"{Fore.LIGHTBLUE_EX}{message}{Style.RESET_ALL}"
        assert stylize_text(message) == expected

    def test_stylize_error_message_without_title(self):
        """Test error message stylization without a title."""
        message = "An error occurred."
        expected = f"{Fore.RED}{message}{Style.RESET_ALL}"
        assert stylize_error_message(message) == expected

    def test_stylize_error_message_with_title(self):
        """Test error message stylization with a title."""
        message = "Invalid input."
        title = "Error"
        expected = f"{Fore.RED}{title}: {message}{Style.RESET_ALL}"
        assert stylize_error_message(message, title) == expected

    def test_stylize_success_message(self):
        """Test success message stylization."""
        message = "Operation successful."
        expected = f"{Fore.GREEN}{message}{Style.RESET_ALL}"
        assert stylize_success_message(message) == expected

    def test_stylize_warning_message(self):
        """Test warning message stylization."""
        message = "This is a warning."
        expected = f"{Fore.LIGHTYELLOW_EX}{message}{Style.RESET_ALL}"
        assert stylize_warning_message(message) == expected

    def test_stylize_tag(self):
        """Test tag stylization."""
        tag = "python"
        expected = f"{Fore.MAGENTA}{tag}{Style.RESET_ALL}"
        assert stylize_tag(tag) == expected


class TestStylingDecorators:
    """Tests for the styling decorators."""

    def test_stylize_errors_decorator(self):
        """Test the @stylize_errors decorator."""
        @stylize_errors
        def get_error_message():
            return "Something went wrong."

        expected = f"{Fore.RED}Something went wrong.{Style.RESET_ALL}"
        assert get_error_message() == expected

    def test_stylize_success_decorator(self):
        """Test the @stylize_success decorator."""
        @stylize_success
        def get_success_message():
            return "Everything is great."

        expected = f"{Fore.GREEN}Everything is great.{Style.RESET_ALL}"
        assert get_success_message() == expected

    def test_stylize_warning_decorator(self):
        """Test the @stylize_warning decorator."""
        @stylize_warning
        def get_warning_message():
            return "Handle with care."

        expected = f"{Fore.LIGHTYELLOW_EX}Handle with care.{Style.RESET_ALL}"
        assert get_warning_message() == expected

    def test_decorator_preserves_function_metadata(self):
        """Test that decorators preserve the wrapped function's metadata."""
        @stylize_errors
        def my_function():
            """This is a docstring."""
            return "message"

        assert my_function.__name__ == 'my_function'
        assert my_function.__doc__ == 'This is a docstring.'
