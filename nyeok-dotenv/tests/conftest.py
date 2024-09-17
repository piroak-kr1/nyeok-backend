import os

from unittest import mock
import pytest


@pytest.fixture(autouse=True)
def clean_environ():
    with mock.patch.dict(os.environ, {}):
        yield
