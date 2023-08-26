"""Stores hardcoded project data."""

from typeguard import typechecked


# pylint: disable=R0903
class HC:
    """Stores hardcoded data."""

    @typechecked
    def __init__(self) -> None:
        """Initialise the hardcoded data."""
        self.indent_spaces: int = 4
        self.json_identifier = "json_"
        self.reconstruct_id = "reconstructed_"
