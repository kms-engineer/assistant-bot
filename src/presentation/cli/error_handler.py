from functools import wraps
from typing import Callable


def handle_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            error_msg = str(e).strip("'\"")
            if "Note" in error_msg:
                return f"Note not found: {error_msg}"
            else:
                return f"Contact not found: {error_msg}"
        except ValueError as e:
            return f"Error: {e}"
        except IndexError as e:
            return f"Error: {e}"
        except IOError as e:
            return f"File error: {e}"
        except Exception as e:
            return f"An error occurred: {type(e).__name__}: {e}"

    return wrapper
