"""Handles the generate commands for a function in a file."""

from typeguard import typechecked


@typechecked
def apply_function_docstring_json_to_py(
    *,
    extension: str,
    file_dir: str,
    filename: str,
    func_name: str,
    iteration: int,
) -> None:
    """
    0. Verifies the <file_dir>/<filename>.py file has a valid Python syntax.
    1. Makes a .json backup of the function of the file
    <file_dir>/<filename>.py
    named:
    <file_dir>/<filename>_func_<function>_backup_docstring_<iteration>.json.
    2. Verifies the docstring contains the argument parameters.
    3. Verifies the docstring contains the argument parameter descriptions.
    4. Verifies the docstring contains the return description.
    5. Applies the docstring of the
    <file_dir>/<filename>_func_<function>_gpt_<iteration>.json
    to the <file_dir>/<filename>.py file
    6. Verifies the <file_dir>/<filename>.py file still has a valid Python
    syntax.
    7. Applies black formatting.
    """
    print("TODO: Apply docstring in function in Python file based on Json.")
    print(extension)
    print(file_dir)
    print(filename)
    print(func_name)
    print(iteration)


@typechecked
def apply_function_json_to_py(
    *,
    extension: str,
    file_dir: str,
    filename: str,
    func_name: str,
    iteration: int,
) -> None:
    """
    0. Verifies the <file_dir>/<filename>.py file has a valid Python syntax.
    1. Makes a .json backup of the function of the file
    <file_dir>/<filename>.py
    named:
    <file_dir>/<filename>_func_<function>_backup_function_<iteration>.json.
    2. Verify all function args are typed.
    3. Verify the return type of the function is specified.
    4. Verifies the docstring contains the argument parameters.
    5. Verifies the docstring contains the argument parameter descriptions.
    6. Verifies the docstring contains the return description.
    7. Optional: Verify the function signature remains unchanged.
    8. Optional: Verify the function AST remains unchanged.
    9. Optional: Verify the decorators remain unchanged.
    10. Optional: Verify the ignore (lint) comments remain unchanged.
    11. Applies the function of the
    <file_dir>/<filename>_func_<function>gpt_<iteration>.json
    file, to the <file_dir>/<filename>.py file
    12. Verifies the <file_dir>/<filename>.py file still has a valid Python
    syntax.
    13. Applies black formatting.

    """
    print("TODO: Apply function from json to function in Python file.")
    print(extension)
    print(file_dir)
    print(filename)
    print(func_name)
    print(iteration)


@typechecked
def apply_test_code_json_for_function_to_py(
    *,
    extension: str,
    file_dir: str,
    filename: str,
    func_name: str,
    iteration: int,
    test_dir: int,
) -> None:
    """
    0. If the <test_dir>/unit_test/<filename>/test_<function>.py exists,
        0.a Verifies the <test_dir>/unit_test/<filename>/test_<function>.py
          file has a valid Python syntax.
        0.b Makes a .json backup of the test file:
        <test_dir>/unit_test/<filename>/test_<function>.py
        named:
        <test_dir>/unit_test/<filename>/test_<function>_backup_<iteration>.json
    2. Verify all function args are typed.
    3. Verify the return type of the function is specified.
    4. Verifies the docstring contains the argument parameters.
    5. Verifies the docstring contains the argument parameter descriptions.
    6. Verifies the docstring contains the return description.
    7. Optional: Verify the function signature remains unchanged.
    8. Optional: Verify the function AST remains unchanged.
    9. Optional: Verify the decorators remain unchanged.
    10. Optional: Verify the ignore (lint) comments remain unchanged.
    11. Applies the function of the
    <file_dir>/<filename>_func_<function>gpt_<iteration>.json
    file, to the <file_dir>/<filename>.py file
    12. Verifies the <file_dir>/<filename>.py file still has a valid Python
    syntax.
    13. Applies black formatting.
    """
    print(
        "TODO: Apply test_code in Python file for function in python"
        + " file based on Json."
    )
    print(extension)
    print(file_dir)
    print(filename)
    print(func_name)
    print(iteration)
    print(test_dir)
