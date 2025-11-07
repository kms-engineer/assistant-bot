from typing import List, Optional, Callable


def select_from_list(
    items: List,
    prompt: str = "Select an option:",
    formatter: Optional[Callable] = None,
    allow_cancel: bool = True
) -> Optional[int]:
    if not items:
        return None

    if formatter is None:
        formatter = str

    # Display options
    print(f"\n{prompt}")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {formatter(item)}")

    if allow_cancel:
        print(f"  0. Cancel")

    # Get user selection
    while True:
        try:
            response = input("\nEnter number: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None

        if not response:
            continue

        try:
            choice = int(response)
        except ValueError:
            print("Please enter a valid number.")
            continue

        # Handle cancel
        if choice == 0 and allow_cancel:
            return None

        # Validate range
        if 1 <= choice <= len(items):
            return choice - 1  # Return 0-based index
        else:
            print(f"Please enter a number between {0 if allow_cancel else 1} and {len(items)}.")


def select_option(prompt: str, options: List[str], allow_cancel: bool = True) -> Optional[int]:
    return select_from_list(items=options, prompt=prompt, allow_cancel=allow_cancel)
