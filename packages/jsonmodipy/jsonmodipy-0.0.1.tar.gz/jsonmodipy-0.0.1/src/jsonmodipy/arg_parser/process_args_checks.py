"""Processes API arguments and performs the requested actions."""
from argparse import Namespace

from typeguard import typechecked


@typechecked
def process_api_args_check(*, args: Namespace) -> None:
    """Processes the arguments and performs the requested actions."""
    if args.get or args.gen or args.improve:
        if not args.filepath:
            raise ValueError(
                "--filepath is required when any action is specified."
            )

        if args.get is not None and args.get not in [
            "class_names",
            "docstring",
            "func_names",
            "json",
            "src_code",
            "test_code",
            "test_names",
        ]:
            raise ValueError(f"Invalid choice for --get action:{args.get}.")

        if args.gen is not None and args.gen not in [
            "json",
            "src_code",
            "docstring",
            "test_code",
            "testnames",
        ]:
            raise ValueError(f"Invalid choice for --gen action:{args.gen}.")

        if args.gen and not (args.function or args.classes):
            raise ValueError(
                "--function or --classes must be provided with --gen action."
            )
    else:
        if not args.filepath:
            raise ValueError("--filepath is required.")
