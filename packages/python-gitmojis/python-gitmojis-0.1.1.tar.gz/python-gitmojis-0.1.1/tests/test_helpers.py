import pytest
from requests import ConnectionError, HTTPError, RequestException

from gitmojis.helpers import get_github_emoji_codes


@pytest.fixture()
def github_api_response():
    return {
        "a": "emoji-a-url",
        "b": "emoji-b-url",
    }


def test_get_github_emoji_codes(requests_json, github_api_response):
    requests_json.return_value = github_api_response

    get_github_emoji_codes.cache_clear()

    assert get_github_emoji_codes() == list(github_api_response.keys())


@pytest.mark.parametrize(
    "requests_error",
    [
        ConnectionError,
        HTTPError,
        RequestException,
    ],
)
def test_get_github_emoji_codes_requests_error(requests_get, requests_error):
    requests_get.side_effect = requests_error

    get_github_emoji_codes.cache_clear()

    assert get_github_emoji_codes() == []
