"""Processes API arguments and performs the requested actions."""
from argparse import Namespace

from typeguard import typechecked

from src.jsonmodipy.file_parsing import get_file_content
from src.jsonmodipy.get.clss import (
    get_class_code,
    get_class_docstring,
    get_class_test_file_code,
    get_class_test_names,
)
from src.jsonmodipy.get.file import (
    get_class_names,
    get_file_docstring,
    get_function_names,
)
from src.jsonmodipy.get.function import (
    get_function_docstring,
    get_function_src_code,
    get_function_test_file_code,
    get_function_test_names,
)


@typechecked
def process_api_args_get(
    *, args: Namespace, extension: str, file_dir: str, filename: str
) -> None:
    """Processes the get arguments and performs the requested actions."""
    process_api_args_get_file(
        args=args, extension=extension, file_dir=file_dir, filename=filename
    )
    process_api_args_get_function(
        args=args, file_dir=file_dir, extension=extension, filename=filename
    )
    process_api_args_get_class(
        args=args, extension=extension, file_dir=file_dir, filename=filename
    )


def process_api_args_get_file(
    *, args: Namespace, extension: str, file_dir: str, filename: str
) -> None:
    """Get file related information.

    If no function are specified, refer to file.
    """
    if args.get == "class_names" and not (args.function or args.clss):
        get_class_names(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
        )
    elif args.get == "docstring" and not (args.function or args.clss):
        # Return empty string if docstring does not exist.
        get_file_docstring(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
        )
    elif args.get == "func_names" and not (args.function or args.clss):
        get_function_names(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
        )
    elif args.get == "json" and not (args.function or args.clss):
        raise NotImplementedError("Error, returning JSON not supported.")
    if args.get == "src_code" and not (args.function or args.clss):
        get_file_content(file_path=f"{file_dir}{file_dir}.py")
    elif args.get == "test_code" and not (args.function or args.clss):
        raise NotImplementedError(
            "Error, returning test files of all functions in a file is not"
            + " supported."
        )
    if args.get == "test_names" and args.function is None:
        raise NotImplementedError(
            "Error, returning test names of all test names of all function in"
            + " a file is not supported."
        )


def process_api_args_get_function(
    *, args: Namespace, extension: str, file_dir: str, filename: str
) -> None:
    """Get function name related information."""
    if args.get == "class_names" and args.function is not None:
        raise NotImplementedError(
            "Error, you gave a function name and asked for class name."
        )
    if args.get == "docstring" and args.function is not None:
        # Return empty string if docstring does not exist.
        get_function_docstring(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            func_name=args.function,
        )
    elif args.get == "func_names" and args.function is not None:
        raise NotImplementedError(
            "Error, you gave a function name and asked for it."
        )
    elif args.get == "json" and args.function is not None:
        raise NotImplementedError("Error, returning JSON not supported.")
    elif args.get == "src_code" and args.function is not None:
        get_function_src_code(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            func_name=args.function,
        )
    elif args.get == "test_code" and args.function is not None:
        get_function_test_file_code(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            func_name=args.function,
        )
    elif args.get == "test_names" and args.function is not None:
        get_function_test_names(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            func_name=args.function,
        )


def process_api_args_get_class(
    *, args: Namespace, extension: str, file_dir: str, filename: str
) -> None:
    """Get class name related information."""
    if args.get == "class_names" and args.clss is not None:
        raise NotImplementedError(
            "Error, you gave a class name and asked for class name."
        )
    if args.get == "docstring" and args.clss is not None:
        # Return empty string if docstring does not exist.
        print("TODO: Return docstring of the class in the file.")
        get_class_docstring(
            class_name=args.clss,
            extension=extension,
            file_dir=file_dir,
            filename=filename,
        )
    elif args.get == "func_names" and args.clss is not None:
        raise NotImplementedError(
            "Error, you gave a class name and asked for it."
        )
    if args.get == "json" and args.clss is not None:
        raise NotImplementedError("Error, returning JSON not supported.")
    if args.get == "src_code" and args.clss is not None:
        print("TODO: Return Python code of the class in the file.")
        get_class_code(
            class_name=args.clss,
            extension=extension,
            file_dir=file_dir,
            filename=filename,
        )
    elif args.get == "test_code" and args.clss is not None:
        print("TODO: Return python test file of the class in the file.")
        get_class_test_file_code(
            class_name=args.clss,
            extension=extension,
            file_dir=file_dir,
            filename=filename,
        )
    elif args.get == "test_names" and args.clss is not None:
        print("TODO: Return python test names of the class in the file.")
        get_class_test_names(
            class_name=args.clss,
            extension=extension,
            file_dir=file_dir,
            filename=filename,
        )
