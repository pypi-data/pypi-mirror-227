"""Handles the get commands for a function in a file."""


from libcst import FunctionDef  # type: ignore[import]
from typeguard import typechecked

from ..file_parsing import load_file_content
from ..get.helper import get_code_for_node
from .helper_function import (
    get_docstring_from_function_node,
    get_function_node_from_file,
)


@typechecked
def get_function_docstring(
    *,
    extension: str,
    file_dir: str,
    filename: str,
    func_name: str,
) -> str:
    """Returns the docstring of a Python function in a python file."""
    file_code: str = load_file_content(
        file_path=f"{file_dir}/{filename}{extension}"
    )
    py_func_node: FunctionDef = get_function_node_from_file(
        file_code=file_code, func_name=func_name
    )

    # pprint(py_func_node)
    func_docstring: str = get_docstring_from_function_node(
        py_func_node=py_func_node
    )
    print(func_docstring)
    return func_docstring


@typechecked
def get_function_src_code(
    *,
    extension: str,
    file_dir: str,
    filename: str,
    func_name: str,
) -> str:
    """Returns the code of a Python function in a python file."""
    file_code: str = load_file_content(
        file_path=f"{file_dir}/{filename}{extension}"
    )
    py_func_node: FunctionDef = get_function_node_from_file(
        file_code=file_code, func_name=func_name
    )
    py_func_str: str = get_code_for_node(some_node=py_func_node)
    print(py_func_str)
    return py_func_str


@typechecked
def get_function_test_file_code(
    *,
    extension: str,
    file_dir: str,
    filename: str,
    func_name: str,
) -> str:
    """Returns the code of a test file that tests a Python function of a python
    file."""
    print("TODO: Return python test file code of the function in the file.")

    print(extension)
    print(file_dir)
    print(filename)
    print(func_name)
    return "TODO"


@typechecked
def get_function_test_names(
    *,
    extension: str,
    file_dir: str,
    filename: str,
    func_name: str,
) -> str:
    """Returns the names of the test functions of the test file that tests a
    Python function of a python file."""
    print("TODO: Return python test names of the function in the file.")
    print(extension)
    print(file_dir)
    print(filename)
    print(func_name)
    return "TODO"
