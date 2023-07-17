import pytest
from starlette.testclient import TestClient

from delvify.models import TaskList
from delvify.schemas import TaskListCreateInternal


def _to_form(tasklist: TaskList) -> TaskListCreateInternal:
    return TaskListCreateInternal(title=tasklist.title, user_email=tasklist.user_email)


@pytest.mark.parametrize(
    "method, url",
    [
        ("POST", "/api/v1/lists"),
        ("GET", "/api/v1/lists"),
        ("GET", "/api/v1/lists/1"),
        ("PUT", "/api/v1/lists/1"),
        ("DELETE", "/api/v1/lists/1"),
    ],
)
def test_forbidden_without_token(method: str, url: str, client: TestClient):
    response = client.request(method, url)
    assert response.status_code == 403
    assert len(response.json()["detail"]) > 0
