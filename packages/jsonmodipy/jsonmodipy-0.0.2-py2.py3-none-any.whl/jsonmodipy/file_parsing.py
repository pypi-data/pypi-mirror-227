"""Loads Python file content into string, and performs checks on Python
files."""
import json
import os
import subprocess  # nosec
from pathlib import Path
from typing import List, Tuple

from typeguard import typechecked

from src.jsonmodipy.PythonStructures import JsonContentType


def split_file_path(*, file_path: str) -> Tuple[str, str, str]:
    """Split a file path into directory path, filename, and extension.

    Args:
        file_path (str): The input file path.

    Returns:
        Tuple[str, str, str]: A tuple containing directory path, filename, and
        extension.
    """
    path_obj: Path = Path(file_path)
    directory_path: str = str(path_obj.parent)
    filename = os.path.splitext(path_obj.name)[0]
    extension = path_obj.suffix

    return directory_path, filename, extension


@typechecked
def get_py_filenames(
    extension: str, folder_path: str, exclude_start: str
) -> List[str]:
    """Get a list of files with the specified extension in a folder, excluding
    those starting with the specified prefix.

    Args:
        extension (str): The desired file extension (e.g., '.py').
        folder_path (str): The path to the folder containing the files.
        exclude_start (str): The prefix to exclude from file names.

    Returns:
        list: A list of files with the specified extension in the folder that
          do not start with the specified prefix.
    """
    files = []
    for file in os.listdir(folder_path):
        if file.endswith(extension) and not file.startswith(exclude_start):
            filename_without_extension = os.path.splitext(file)[0]
            files.append(filename_without_extension)
    return files


@typechecked
def load_file_content(file_path: str) -> str:
    """Load the content of a file into a single string.

    Args:
        file_path (str): The path to the file to be loaded.

    Returns:
        str: The content of the file as a single string.

    Raises:
        FileNotFoundError: If the specified file_path does not exist.
        IOError: If there's an error reading the file.
    """
    with open(file_path, encoding="utf-8") as file:
        content = file.read()
    return content


@typechecked
def write_dict_to_json(data: JsonContentType, filepath: str) -> None:
    """Write a dictionary to a JSON file.

    Args:
        data (Dict[str, Any]): The dictionary to be written.
        filename (str): The name of the JSON file to create or overwrite.
    """
    with open(filepath, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)


@typechecked
def load_dict_from_json(
    filename: str,
) -> JsonContentType:
    """Load a dictionary from a JSON file.

    Args:
        filename (str): The name of the JSON file to read from.

    Returns:
        Dict[str, Any]: The dictionary loaded from the JSON file.
    """
    with open(filename, encoding="utf-8") as json_file:
        data: JsonContentType = json.load(json_file)
    return data


@typechecked
def format_python_file(file_path: str) -> None:
    """Format a Python file using the Black code formatter.

    Args:
        file_path (str): Path to the Python file.
    """
    # TODO: verify black formatting was successful.
    subprocess.run(
        ["black", file_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )  # nosec


@typechecked
def get_file_content(file_path: str) -> str:
    """Get the content of the specified file.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        str: Content of the file if found. Raises error otherwise.
    """
    if os.path.exists(file_path):
        with open(file_path, encoding="utf-8") as file:
            content = file.read()
        return content
    raise FileNotFoundError(f"File '{file_path}' not found.")


@typechecked
def set_file_content(file_path: str, content: str) -> None:
    """Set the content of the specified file.

    Args:
        file_path (str): Path to the Python file.
        content (str): Content to write into the file.
    """

    if os.path.exists(file_path):
        raise FileExistsError(f"File '{file_path}' already exists.")

    with open(file_path, "w", encoding="utf-8") as file:
        # file.write(content)
        file.write(content)


@typechecked
def delete_file_if_exists(file_path: str) -> None:
    """Delete a file if it exists.

    :param file_path: The path to the file to be deleted.
    :type file_path: str
    """
    if os.path.exists(file_path):
        os.remove(file_path)
