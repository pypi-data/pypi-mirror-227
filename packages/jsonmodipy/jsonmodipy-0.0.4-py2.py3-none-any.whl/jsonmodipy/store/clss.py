"""Handles the generate commands for a class in a file."""

from typeguard import typechecked


@typechecked
def store_class_docstring(
    *,
    extension: str,
    class_name: str,
    file_dir: str,
    filename: str,
) -> None:
    """
    0. Verifies the <file_dir>/<filename>.py file has a valid Python syntax.
    1. Makes a .json backup of the class of the file
    <file_dir>/<filename>.py
    named:
    <file_dir>/<filename>_class_<class>_backup_docstring_<iteration>.json.
    2. Verifies the docstring contains the argument parameters.
    3. Verifies the docstring contains the argument parameter descriptions.
    4. Verifies the docstring contains the return description.
    5. Applies the docstring of the
    <file_dir>/<filename>_class_<class>gpt_<iteration>.json
    to the <file_dir>/<filename>.py file
    6. Verifies the <file_dir>/<filename>.py file still has a valid Python
    syntax.
    7. Applies black formatting.

    """
    print("TODO: Apply docstring in class in Python file based on Json.")
    print(extension)
    print(file_dir)
    print(filename)
    print(class_name)


@typechecked
def store_class_src_code(
    *,
    extension: str,
    class_name: str,
    file_dir: str,
    filename: str,
) -> None:
    r"""
    0. Verifies the <file_dir>/<filename>.py file has a valid Python syntax.
    1. Makes a .json backup of the class of the file
    <file_dir>/<filename>.py
    named:
    <file_dir>/<filename>_class\_<class>_backup_class_<iteration>.json.
    2. Verify all class args are typed.
    3. Verify the return type of the class is specified.
    4. Verifies the docstring contains the argument parameters.
    5. Verifies the docstring contains the argument parameter descriptions.
    6. Verifies the docstring contains the return description.
    7. Optional: Verify the class signature remains unchanged.
    8. Optional: Verify the class AST remains unchanged.
    9. Optional: Verify the decorators remain unchanged.
    10. Optional: Verify the ignore (lint) comments remain unchanged.
    11. Applies the class of the
    <file_dir>/<filename>_class_<class>gpt_<iteration>.json
    file, to the <file_dir>/<filename>.py file
    12. Verifies the <file_dir>/<filename>.py file still has a valid Python
    syntax.
    13. Applies black formatting.
    """
    print("TODO: Apply class from json to class in Python file.")
    print(extension)
    print(file_dir)
    print(filename)
    print(class_name)


@typechecked
def store_class_test_file_code(
    *,
    extension: str,
    class_name: str,
    file_dir: str,
    filename: str,
    test_dir: int,
) -> None:
    """
    0. If the <test_dir>/unit_test/<filename>/test_<class>.py exists,
        0.a Verifies the <test_dir>/unit_test/<filename>/test_<class>.py
          file has a valid Python syntax.
        0.b Makes a .json backup of the test file:
        <test_dir>/unit_test/<filename>/test_<class>.py
        named:
        <test_dir>/unit_test/<filename>/test_<class>_backup_<iteration>.json
    2. Verify all class args are typed.
    3. Verify the return type of the class is specified.
    4. Verifies the docstring contains the argument parameters.
    5. Verifies the docstring contains the argument parameter descriptions.
    6. Verifies the docstring contains the return description.
    7. Optional: Verify the class signature remains unchanged.
    8. Optional: Verify the class AST remains unchanged.
    9. Optional: Verify the decorators remain unchanged.
    10. Optional: Verify the ignore (lint) comments remain unchanged.
    11. Applies the class of the
    <file_dir>/<filename>_class_<class>gpt_<iteration>.json
    file, to the <file_dir>/<filename>.py file
    12. Verifies the <file_dir>/<filename>.py file still has a valid Python
    syntax.
    13. Applies black formatting.
    """
    print(
        "TODO: Apply test_code in Python file for class in python"
        + " file based on Json."
    )
    print(extension)
    print(file_dir)
    print(filename)
    print(class_name)
    print(test_dir)
