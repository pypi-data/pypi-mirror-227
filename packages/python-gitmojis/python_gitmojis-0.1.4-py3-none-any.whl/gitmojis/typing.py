from enum import Enum
from typing import NamedTuple


class GitmojiFieldCheck(NamedTuple):
    """A named tuple to represent the status of a Gitmoji field value check."""

    result: bool
    error_message: str


class SemVerLevel(Enum):
    """An enum to represent Semantic Versioning levels."""

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
