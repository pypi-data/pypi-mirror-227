import importlib

import pytest


def test_import():
    try:
        importlib.import_module("gitmojis")
    except (ImportError, ModuleNotFoundError):
        pytest.fail("The package can't be imported.")
