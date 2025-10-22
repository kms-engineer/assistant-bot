from functools import wraps
from typing import Callable

from colorama import Fore, Style


def stylize_text(message: str):
    return f"{Fore.LIGHTBLUE_EX}{message}{Style.RESET_ALL}"


def stylize_error_message(message: str, title: str = None):
    if title:
        return f"{Fore.RED}{title}: {message}{Style.RESET_ALL}"

    return f"{Fore.RED}{message}{Style.RESET_ALL}"


def stylize_success_message(message: str):
    return f"{Fore.GREEN}{message}{Style.RESET_ALL}"


def stylize_warning_message(message: str):
    return f"{Fore.LIGHTYELLOW_EX}{message}{Style.RESET_ALL}"


def stylize_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        return stylize_error_message(message=func(*args, **kwargs))

    return wrapper


def stylize_success(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        return stylize_success_message(message=func(*args, **kwargs))

    return wrapper


def stylize_warning(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        return stylize_warning_message(message=func(*args, **kwargs))

    return wrapper
