"""Processes API arguments and performs the requested actions."""
from argparse import Namespace

from typeguard import typechecked

from src.jsonmodipy.apply.clss import (
    apply_class_docstring_json_to_py,
    apply_class_json_to_py,
    apply_test_code_json_for_class_to_py,
)
from src.jsonmodipy.apply.file import (
    apply_file_docstring_json_to_py,
    apply_file_json_to_py,
    apply_test_code_json_for_file_to_py,
)
from src.jsonmodipy.apply.function import (
    apply_function_docstring_json_to_py,
    apply_function_json_to_py,
    apply_test_code_json_for_function_to_py,
)


@typechecked
def process_api_args_gen(
    *, args: Namespace, extension: str, file_dir: str, filename: str
) -> None:
    """Processes the gen arguments and performs the requested actions."""
    process_api_args_apply_file(
        args=args,
        extension=extension,
        file_dir=file_dir,
        filename=filename,
    )
    process_api_args_apply_function(
        args=args,
        extension=extension,
        file_dir=file_dir,
        filename=filename,
        func_name=args.function,
    )
    process_api_args_apply_class(
        args=args,
        extension=extension,
        file_dir=file_dir,
        filename=filename,
        class_name=args.clss,
    )


def process_api_args_apply_file(
    *, args: Namespace, extension: str, file_dir: str, filename: str
) -> None:
    """Apply file related generation actions.

    If no function are specified, refer to file.
    """
    if args.apply == "class_names" and not (args.function or args.clss):
        raise NotImplementedError("Error, will not apply class_names")
    if args.apply == "docstring" and not (args.function or args.clss):
        apply_file_docstring_json_to_py(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            iteration=args.iteration,
        )
    elif args.apply == "func_names" and not (args.function or args.clss):
        raise NotImplementedError("Error, will not apply func_names")
    if args.apply == "json" and not (args.function or args.clss):
        raise NotImplementedError(
            "Error, the thing that is applied, is a json, so will not apply a "
            + "json to a json."
        )
    if args.apply == "src_code" and not (args.function or args.clss):
        apply_file_json_to_py(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            iteration=args.iteration,
        )
    elif args.apply == "test_code" and not (args.function or args.clss):
        apply_test_code_json_for_file_to_py(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            iteration=args.iteration,
            test_dir=args.test_dir,
        )
    elif args.apply == "test_names" and not (args.function or args.clss):
        raise NotImplementedError("Error, will not apply test_names")


def process_api_args_apply_function(
    *,
    args: Namespace,
    extension: str,
    file_dir: str,
    filename: str,
    func_name: str,
) -> None:
    """Apply function name related generation actions."""
    if args.apply == "class_names" and args.function is not None:
        raise NotImplementedError(
            "Error, will not apply class_names for function."
        )
    if args.apply == "docstring" and args.function is not None:
        apply_function_docstring_json_to_py(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            func_name=func_name,
            iteration=args.iteration,
        )
    elif args.apply == "func_names" and args.function is not None:
        raise NotImplementedError(
            "Error, will not apply func_names for function"
        )
    if args.apply == "json" and args.function is not None:
        raise NotImplementedError(
            "Error, the thing that is applied, is a json, so will not apply a "
            + "json to a json."
        )
    if args.apply == "src_code" and args.function is not None:
        apply_function_json_to_py(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            func_name=func_name,
            iteration=args.iteration,
        )
    elif args.apply == "test_code" and args.function is not None:
        apply_test_code_json_for_function_to_py(
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            func_name=func_name,
            iteration=args.iteration,
            test_dir=args.test_dir,
        )
    elif args.apply == "test_names" and args.function is not None:
        raise NotImplementedError(
            "Error, will not apply test_names for function."
        )


def process_api_args_apply_class(
    *,
    args: Namespace,
    extension: str,
    file_dir: str,
    filename: str,
    class_name: str,
) -> None:
    """Apply class name related generation actions."""
    if args.apply == "class_names" and args.clss is not None:
        raise NotImplementedError(
            "Error, will not apply class_names for class."
        )
    if args.apply == "docstring" and args.clss is not None:
        print("TODO: Apply docstring in class in Python file based on Json.")
        apply_class_docstring_json_to_py(
            class_name=class_name,
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            iteration=args.iteration,
        )
    elif args.apply == "func_names" and args.clss is not None:
        raise NotImplementedError("Error, will not apply func_names for class")
    if args.apply == "json" and args.clss is not None:
        raise NotImplementedError(
            "Error, the thing that is applied, is a json, so will not apply a "
            + "json to a json."
        )
    if args.apply == "src_code" and args.clss is not None:
        apply_class_json_to_py(
            class_name=class_name,
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            iteration=args.iteration,
        )
    elif args.apply == "test_code" and args.clss is not None:
        apply_test_code_json_for_class_to_py(
            class_name=class_name,
            extension=extension,
            file_dir=file_dir,
            filename=filename,
            iteration=args.iteration,
            test_dir=args.test_dir,
        )
    elif args.apply == "test_names" and args.clss is not None:
        raise NotImplementedError(
            "Error, will not apply test_names for class."
        )
