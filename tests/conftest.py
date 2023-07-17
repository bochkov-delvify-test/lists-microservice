import pytest
from httpx import Client
from starlette.testclient import TestClient

from delvify.main import ms


@pytest.fixture()
def client() -> Client:
    return TestClient(ms)
