import json
import re
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Dict, List, Optional, Union

import requests
from emoji import is_emoji
from requests import ConnectionError, HTTPError, RequestException

from .exceptions import GitmojiFieldValidationError, GitmojisJsonFormatError
from .helpers import get_github_emoji_codes
from .typing import GitmojiFieldCheck, SemVerLevel


@dataclass
class Gitmoji:
    """A class to represent a Gitmoji data."""

    emoji: str
    code: str
    description: str
    name: Optional[str] = None
    semver: Optional[Union[str, SemVerLevel]] = None

    def __post_init__(self) -> None:
        """Perform post-init actions."""
        self._check_fields()

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, None]]) -> "Gitmoji":
        """Return a Gitmoji object using the field data passed as a dict."""
        gitmoji_data = {
            field_name: field_value
            for field_name, field_value in data.items()
            if field_name in cls.__dataclass_fields__
        }
        return cls(**gitmoji_data)  # type: ignore

    def _check_fields(self) -> None:
        """Perform a field check for all the checkable fields of the dataclass.

        A field FIELD is checkable if `_check_FIELD` method is implemented.
        """
        for field in fields(self):
            field_name = field.name
            check_method_name = f"_check_{field_name}"
            if hasattr(self, check_method_name):
                field_check = getattr(self, check_method_name)()
                if not field_check.result:
                    field_value = getattr(self, field_name)
                    raise GitmojiFieldValidationError(
                        f"Invalid value for the {field_name!r} field: {field_value!r}. "
                        f"{field_check.error_message}"
                    )

    def _check_emoji(self) -> GitmojiFieldCheck:
        """Validate the `code` field value of the dataclass instance."""
        # NOTE: `emoji.is_emoji()` utility returns a false negative result for some of
        # the Gitmojis. This regards all the Gitmojis ending with \ufe0f (the variation
        # selector; see https://stackoverflow.com/a/38100803/18713601), which is NOT
        # found in the corresponding emojis collected in the `emoji` package. That is
        # why potentially invalid emojis are first stripped to remove the \ufe0f suffix,
        # and the check is repeated.
        result = is_emoji(self.emoji)
        if not result and self.emoji.endswith("\ufe0f"):
            result = is_emoji(self.emoji.rstrip("\ufe0f"))
        error_message = f"{self.emoji!r} is not a valid emoji."
        return GitmojiFieldCheck(result, error_message)

    def _check_code(self) -> GitmojiFieldCheck:
        """Validate the `code` field value of the dataclass instance."""
        github_emoji_codes = get_github_emoji_codes()
        result = (
            re.match(
                rf":({'|'.join(github_emoji_codes)}):"
                if github_emoji_codes
                else r":[-\+\w]+:",
                self.code,
            )
            is not None
        )
        error_message = (
            "The value must match the emoji's code regular expression as well as be "
            "a valid emoji name (i.e., the one accessible via the GitHub API)."
        )
        return GitmojiFieldCheck(result, error_message)

    def _check_description(self) -> GitmojiFieldCheck:
        """Validate the `description` field value of the dataclass instance."""
        result = self.description[:1].isupper() and self.description.endswith(".")
        error_message = (
            "The value must start with a capital letter and end with a period."
        )
        return GitmojiFieldCheck(result, error_message)

    def _check_name(self) -> GitmojiFieldCheck:
        """Validate the `name` field value of the dataclass instance."""
        valid_name = self.code[1:-1].replace("_", "-")
        if self.name is None:
            self.name = valid_name
        result = self.name == valid_name
        error_message = (
            "The value is inconsistent with the value of 'code' field; 'name' should "
            "be the same as the code except colons and underscores. The latter must be "
            f"replaced by dashes. So, the valid 'name' is: {valid_name!r}."
        )
        return GitmojiFieldCheck(result, error_message)

    def _check_semver(self) -> GitmojiFieldCheck:
        """Validate the `semver` field value of the dataclass instance."""
        if isinstance(self.semver, str):
            # Attempt to convert the value to SemVerLevel enum.
            try:
                self.semver = SemVerLevel(self.semver)
            except ValueError:
                result = False
            else:
                result = True
        else:
            result = isinstance(self.semver, SemVerLevel) or self.semver is None
        error_message = "The value must be a string {}, {} member, or None.".format(
            "/".join([f'"{level.value}"' for level in SemVerLevel]),
            SemVerLevel.__name__,
        )
        return GitmojiFieldCheck(result, error_message)


def get_gitmojis() -> List[Gitmoji]:
    """Return a list of Gitmoji objects representing the current state of the API."""
    try:
        response = requests.get("https://gitmoji.dev/api/gitmojis")
        response.raise_for_status()
    except (ConnectionError, HTTPError, RequestException):
        gitmojis_json_path = (
            Path(__file__).resolve().parent / "assets" / "gitmojis.json"
        )
        with gitmojis_json_path.open() as gitmojis_json:
            gitmoji_json = json.load(gitmojis_json)
    else:
        gitmoji_json = response.json()

    gitmojis = gitmoji_json.get("gitmojis")
    if gitmojis is None:
        raise GitmojisJsonFormatError("Gitmoji data format isn't valid.")

    return [Gitmoji.from_dict(gitmoji) for gitmoji in gitmojis]


gitmojis = get_gitmojis()
