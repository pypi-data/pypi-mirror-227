"""Tests whether the adder function indeed adds 2 to a given input."""
import unittest
from typing import List

from typeguard import typechecked

from jsonmodipy.file_parsing import (  # type: ignore[import]
    delete_file_if_exists,
    get_file_content,
    get_py_filenames,
)
from jsonmodipy.HC import HC  # type: ignore[import]
from jsonmodipy.PythonGetter import PythonGetter  # type: ignore[import]


class Test_adder(unittest.TestCase):
    """Object used to test a parse_creds function."""

    # Initialize test object
    @typechecked
    def __init__(self, *args, **kwargs):  # type:ignore[no-untyped-def]
        super().__init__(*args, **kwargs)
        self.hc: HC = HC()
        self.file_dir: str = "test/test_files/"
        self.raw_filenames: List[str] = get_py_filenames(
            extension=".py",
            folder_path=self.file_dir,
            exclude_start=self.hc.reconstruct_id,
        )

    @typechecked
    def testcode_to_structure(self) -> None:
        """Tests if add_two function adds 2 to an integer."""
        for raw_filename in self.raw_filenames:
            if raw_filename == "documentation_and_class_and_methods":
                print(raw_filename)
                # Get Python filecontent from filepath.
                python_content: str = get_file_content(
                    f"{self.file_dir}{raw_filename}.py"
                )

                json_dummy_filepath: str = (
                    f"{self.file_dir}"
                    + f"{self.hc.reconstruct_id}{raw_filename}.json"
                )

                delete_file_if_exists(file_path=json_dummy_filepath)
                # Create PythonGetter.
                PythonGetter(
                    python_content=python_content,
                    file_dir=self.file_dir,
                    raw_filename=raw_filename,
                )

        self.assertEqual(1, 2)
