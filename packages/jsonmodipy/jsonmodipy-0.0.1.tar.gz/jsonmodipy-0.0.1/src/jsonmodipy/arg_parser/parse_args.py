"""Parses CLI arguments for the API interactions."""
import argparse

from typeguard import typechecked


@typechecked
def parse_api_args() -> argparse.Namespace:
    """Reads command line arguments and converts them into Python arguments."""
    parser = argparse.ArgumentParser(
        description="CLI for handling JSON, Python code, and docstrings."
    )

    # Group for getting information
    get_group = parser.add_argument_group(
        "Get Information from target repository"
    )
    get_group.add_argument(
        "--get",
        choices=[
            "class_names",
            "json",
            "func_names",
            "src_code",
            "docstring",
            "test_code",
            "testnames",
        ],
        help="Get information from the target repository.",
    )

    # Group for genting information
    gen_group = parser.add_argument_group("Store Json from ChatGPT")
    gen_group.add_argument(
        "--store",
        choices=["docstring", "src_code", "test_code"],
        help=(
            "Store Json file(s) from ChatGPT into the target repository "
            + "Python code."
        ),
    )

    # Group for genting information
    gen_group = parser.add_argument_group("Apply Json to Python")
    gen_group.add_argument(
        "--apply",
        choices=["docstring", "src_code", "test_code"],
        help=(
            "Apply Json files from ChatGPT into the target repository "
            + "Python code."
        ),
    )

    # Group for getting information
    get_group = parser.add_argument_group("ChatGPT iteration number")
    get_group.add_argument(
        "--iteration",
        help="Perform actions on some edit iteration.",
    )

    # Common arguments
    parser.add_argument(
        "--filepath",
        required=True,
        help="Path to the file with function, a docstring, or classes.",
        type=str,
    )

    parser.add_argument(
        "--test-dir",
        required=True,
        help="Path to the unit test dir.",
        type=str,
    )

    parser.add_argument(
        "--function",
        help=(
            "List of function names (optionally: in a file) that you want "
            + "to consider."
        ),
    )

    parser.add_argument(
        "--clss",
        help=(
            "List of classes (optionally: in a file) that you want to consider"
            ". E.g. --classes Plant Sky"
        ),
    )

    args = parser.parse_args()

    return args
