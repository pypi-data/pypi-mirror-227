"""Handles the get commands for a function in a file."""


from typeguard import typechecked


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
    print("TODO: Return Python code of the function in the file.")
    print(extension)
    print(file_dir)
    print(filename)
    print(func_name)
    return "TODO"


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
