"""Handles the get commands for a Python file."""

from typing import List

from typeguard import typechecked


@typechecked
def get_class_names(
    *,
    extension: str,
    file_dir: str,
    filename: str,
) -> List[str]:
    """Returns all the class names of a python file."""
    print("TODO: Return class names of Python file.")
    return [extension, file_dir, filename]


@typechecked
def get_function_names(
    *,
    extension: str,
    file_dir: str,
    filename: str,
) -> List[str]:
    """Returns all the function names of a python file."""
    print("TODO: Return function names of Python file.")
    return [extension, file_dir, filename]


@typechecked
def get_file_docstring(
    *,
    extension: str,
    file_dir: str,
    filename: str,
) -> str:
    """Returns the docstring of a python file without quotations.

    Return empty string if it does not exist.
    """
    print("TODO: Return docstring of Python file.")
    print(extension)
    print(file_dir)
    print(filename)
    return "TODO"


@typechecked
def get_file_content(
    *,
    extension: str,
    file_dir: str,
    filename: str,
) -> str:
    """Returns the file content of a python file."""
    print("TODO: Return Python code of file.")
    print(extension)
    print(file_dir)
    print(filename)
    return "TODO"
