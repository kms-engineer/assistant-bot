from functools import wraps
from typing import Callable


def handle_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return f"Contact not found: {e}"
        except ValueError as e:
            return f"Error: {e}"
        except IndexError as e:
            return f"Error: {e}"
        except IOError as e:
            return f"File error: {e}"
        except Exception as e:
            return f"An error occurred: {type(e).__name__}: {e}"

    return wrapper
