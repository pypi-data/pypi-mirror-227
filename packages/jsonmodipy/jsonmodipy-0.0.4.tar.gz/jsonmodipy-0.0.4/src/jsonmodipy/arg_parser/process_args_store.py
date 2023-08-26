"""Processes API arguments and performs the requested actions."""
from argparse import Namespace

from typeguard import typechecked

from ..store.clss import (
    store_class_docstring,
    store_class_src_code,
    store_class_test_file_code,
)
from ..store.file import (
    store_file_docstring_to_json,
    store_file_to_json,
    store_test_codes_for_file_to_jsons,
)
from ..store.function import (
    store_function_docstring,
    store_function_src_code,
    store_test_code_json_for_function,
)


@typechecked
def process_api_args_store(
    *, args: Namespace, extension: str, file_dir: str, filename: str
) -> None:
    """Processes the store arguments and performs the requested actions."""
    process_api_args_store_file(
        args=args, extension=extension, file_dir=file_dir, filename=filename
    )
    process_api_args_store_function(
        args=args, extension=extension, file_dir=file_dir, filename=filename
    )
    process_api_args_store_class(
        args=args, extension=extension, file_dir=file_dir, filename=filename
    )


def process_api_args_store_file(
    *, args: Namespace, extension: str, file_dir: str, filename: str
) -> None:
    """Get file related information.

    If no function are specified, refer to file.
    """
    if args.store == "class_names" and not (args.function or args.clss):
        raise NotImplementedError(
            "Error, not storing the class names of a src file in a json."
        )
    if args.store == "docstring" and not (args.function or args.clss):
        # Return empty string if docstring does not exist.
        store_file_docstring_to_json(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
        )
    elif args.store == "func_names" and not (args.function or args.clss):
        raise NotImplementedError(
            "Error, not storing the function names of a src file in a json."
        )
    elif args.store == "json" and not (args.function or args.clss):
        raise NotImplementedError(
            "Error, the code is always stored as a json, so not storing a json"
            "of a json."
        )
    if args.store == "src_code" and not (args.function or args.clss):
        store_file_to_json(
            file_dir=file_dir, filename=filename, extension=extension
        )
    elif args.store == "test_code" and not (args.function or args.clss):
        store_test_codes_for_file_to_jsons(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            test_dir=args.test_dir,
        )
    if args.store == "test_names" and args.function is None:
        raise NotImplementedError(
            "Error, returning test names of all test names of all function in"
            + " a file is not supported."
        )


def process_api_args_store_function(
    *, args: Namespace, extension: str, file_dir: str, filename: str
) -> None:
    """Get function name related information."""
    if args.store == "class_names" and args.function is not None:
        raise NotImplementedError(
            "Error, you gave a function name and asked for class name."
        )
    if args.store == "docstring" and args.function is not None:
        # Return empty string if docstring does not exist.
        store_function_docstring(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            func_name=args.function,
        )
    elif args.store == "func_names" and args.function is not None:
        raise NotImplementedError(
            "Error, you gave a function name and asked for it."
        )
    elif args.store == "json" and args.function is not None:
        raise NotImplementedError(
            "Error, the code is always stored as a json, so not storing a json"
            "of a json."
        )
    elif args.store == "src_code" and args.function is not None:
        store_function_src_code(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            func_name=args.function,
        )
    elif args.store == "test_code" and args.function is not None:
        store_test_code_json_for_function(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            func_name=args.function,
            test_dir=args.test_dir,
        )
    elif args.store == "test_names" and args.function is not None:
        raise NotImplementedError(
            "Error, not storing the function names of a test file in a json."
        )


def process_api_args_store_class(
    *, args: Namespace, extension: str, file_dir: str, filename: str
) -> None:
    """Get class name related information."""
    if args.store == "class_names" and args.clss is not None:
        raise NotImplementedError(
            "Error, you gave a class name and asked for class name."
        )
    if args.store == "docstring" and args.clss is not None:
        # Return empty string if docstring does not exist.
        print("TODO: Return docstring of the class in the file.")

        store_class_docstring(
            class_name=args.clss,
            extension=extension,
            file_dir=file_dir,
            filename=filename,
        )
    elif args.store == "func_names" and args.clss is not None:
        raise NotImplementedError(
            "Error, you gave a class name and asked for it."
        )
    if args.store == "json" and args.clss is not None:
        raise NotImplementedError(
            "Error, the code is always stored as a json, so not storing a json"
            "of a json."
        )
    if args.store == "src_code" and args.clss is not None:
        store_class_src_code(
            class_name=args.clss,
            extension=extension,
            file_dir=file_dir,
            filename=filename,
        )
    elif args.store == "test_code" and args.clss is not None:
        print("TODO: Return python test file of the class in the file.")
        store_class_test_file_code(
            class_name=args.clss,
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            test_dir=args.test_dir,
        )
    elif args.store == "test_names" and args.clss is not None:
        raise NotImplementedError(
            "Error, not storing the function names of the tests that are "
            + "written for a class, as a json."
        )
