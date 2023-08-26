"""Handles the get commands for a function in a file."""

from libcst import FunctionDef, parse_module  # type: ignore[import]
from typeguard import typechecked

from ..file_parsing import load_file_content
from ..get.helper import get_code_for_node


@typechecked
def get_function_docstring(
    *,
    extension: str,
    file_dir: str,
    filename: str,
    func_name: str,
) -> str:
    """Returns the docstring of a Python function in a python file."""
    print("TODO: Return function docstring.")
    print(extension)
    print(file_dir)
    print(filename)
    print(func_name)

    return "TODO"


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
def get_function_node_from_file(
    *, file_code: str, func_name: str
) -> FunctionDef:
    """Load and return the FunctionDef node of a function from a Python file.

    Args:
        file_code (str): The source code of the Python file.
        func_name (str): The name of the function to retrieve.

    Returns:
        FunctionDef: The FunctionDef node of the specified function from the
        file, or None if not found.
    """
    module = parse_module(file_code)
    for assignment in module.body:
        matching_functions = [
            assignment
            for assignment in module.body
            if isinstance(assignment, FunctionDef)
            and assignment.name.value == func_name
        ]

    if len(matching_functions) == 0:
        raise ValueError(f"Function '{func_name}' not found in the file.")
    if len(matching_functions) > 1:
        raise ValueError(
            f"More than one function with name '{func_name}' found in file."
        )

    return matching_functions[0]


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
