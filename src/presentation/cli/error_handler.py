from functools import wraps
from typing import Callable

from src.application.exceptions.base import StorageException
from src.domain.utils.styles_utils import stylize_error_message, stylize_success_message


def handle_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return stylize_success_message(func(*args, **kwargs))
        except KeyError as e:
            error_msg = str(e).strip("'\"")
            if "Note" in error_msg:
                return stylize_error_message(title='Note not found', message=error_msg)
            else:
                return stylize_error_message(title='Contact not found', message=error_msg)
        except (ValueError, IndexError) as e:
            return stylize_error_message(title='Error', message=str(e))
        except StorageException as e:
            return stylize_error_message(title='Storage error', message=str(e))
        except IOError as e:
            return stylize_error_message(title='File error', message=str(e))
        except Exception as e:
            return stylize_error_message(title='An error occurred', message=f'{type(e).__name__}: {e}')

    return wrapper
