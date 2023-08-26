"""Handles the get commands for a function in a file."""

from typing import Tuple

from libcst import (  # type: ignore[import]
    Expr,
    FunctionDef,
    IndentedBlock,
    SimpleStatementLine,
    SimpleString,
    parse_module,
)
from typeguard import typechecked


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
def get_docstring_from_function_node(*, py_func_node: FunctionDef) -> str:
    """Get the docstring node from the function node."""
    # We start by checking if the body of the function node is well structured.
    if isinstance(py_func_node.body, IndentedBlock):
        func_body: IndentedBlock = py_func_node.body

        # Within the function's body, we want to look at the lines of code.
        if isinstance(func_body.body, tuple):
            func_code_lines: Tuple = func_body.body  # type: ignore[type-arg]

            # We focus on the first line of code in the function
            if isinstance(func_code_lines[0], SimpleStatementLine):
                first_func_code_line = func_code_lines[0]

                # On this line, we are interested in the first element.
                if isinstance(first_func_code_line.body[0], Expr):
                    expr_node = first_func_code_line.body[0]

                    # Within this expression, we're checking if there's a
                    # string value.
                    if isinstance(expr_node.value, SimpleString):
                        # If we find a string, it means we've likely found the
                        #  docstring and we return its value.
                        return str(expr_node.value.value)

    # If no docstring is found through these checks, we return an empty string
    return ""
