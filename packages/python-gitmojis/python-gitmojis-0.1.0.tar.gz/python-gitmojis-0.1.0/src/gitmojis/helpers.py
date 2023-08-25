import re
from functools import lru_cache
from typing import List

import requests
from requests import ConnectionError, HTTPError, RequestException


@lru_cache(maxsize=None)
def get_github_emoji_codes() -> List[str]:
    """Return a list of emoji codes available in the GitHub markdown language."""
    try:
        response = requests.get("https://api.github.com/emojis")
        response.raise_for_status()
    except (ConnectionError, HTTPError, RequestException):
        github_emoji_codes = {}
    else:
        github_emoji_codes = response.json()
    return [re.escape(code) for code in list(github_emoji_codes.keys())]
