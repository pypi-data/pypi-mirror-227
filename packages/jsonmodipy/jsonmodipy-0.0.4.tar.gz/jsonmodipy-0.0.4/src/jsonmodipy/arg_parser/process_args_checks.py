"""Processes API arguments and performs the requested actions."""
from argparse import Namespace

from typeguard import typechecked


@typechecked
def process_api_args_check(*, args: Namespace) -> None:
    """Processes the arguments and performs the requested actions."""
    if args.get or args.store or args.apply:
        if not args.filepath:
            raise ValueError(
                "--filepath is required when any action is specified."
            )

        # pylint: disable=R0801
        if args.get is not None and args.get not in [
            "class_names",
            "docstring",
            "func_names",
            "json",
            "src_code",
            "test_code",
            "testnames",
        ]:
            raise ValueError(f"Invalid choice for --get action:{args.get}.")

        if args.store is not None and args.store not in [
            "docstring",
            "src_code",
            "test_code",
        ]:
            raise ValueError(
                f"Invalid choice for --store action:{args.store}."
            )

        if args.apply is not None and args.apply not in [
            "docstring",
            "src_code",
            "test_code",
        ]:
            raise ValueError(
                "--function or --classes must be provided with --gen action."
            )
    else:
        if not args.filepath:
            raise ValueError("--filepath is required.")
