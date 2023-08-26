"""Prints an object as text completely."""
from typing import Any

from typeguard import typechecked


@typechecked
def pretty_print(data: Any, indent: int = 0) -> None:
    """Recursively pretty prints data, converting objects with __dict__ to
    dictionaries.

    Args:
        data (Any): The data to be pretty printed.
        indent (int, optional): The current indentation level. Default is 0.

    Returns:
        None
    """
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{' ' * indent}{key}:")
            pretty_print(value, indent + 2)
    elif hasattr(data, "__dict__"):
        pretty_print(data.__dict__, indent)
    elif isinstance(data, list):
        for item in data:
            print(f"{' ' * indent}-")
            pretty_print(item, indent + 2)
    else:
        print(f"{' ' * indent}{data}")
