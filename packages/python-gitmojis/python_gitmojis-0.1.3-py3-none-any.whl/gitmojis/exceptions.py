class GitmojiError(Exception):
    """A base for all the exceptions defined in the package."""


class GitmojiFieldValidationError(GitmojiError):
    """Raised when check of a Gitmoji's field validation fails."""


class GitmojisJsonFormatError(GitmojiError):
    """Raised when Gitmoji JSON data format is invalid."""
