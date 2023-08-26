"""Helpes the get commands."""

from typing import Union

import libcst as cst  # type: ignore[import]
from libcst import ClassDef, FunctionDef
from typeguard import typechecked


@typechecked
def get_code_for_node(*, some_node: Union[FunctionDef, ClassDef]) -> str:
    """Load and return the source code of a function from a Python file.

    Args:
        some_node: The path to the Python file.
        func_name (str): The name of the function to retrieve.

    Returns:
        str: The source code of the specified node of the CST.
    """
    node_code: str = cst.Module([]).code_for_node(some_node)
    return node_code
