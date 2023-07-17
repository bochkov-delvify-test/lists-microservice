from datetime import datetime

import pytest
from httpx import Client
from starlette.testclient import TestClient

from delvify.main import ms
from delvify.models import TaskList, Task


@pytest.fixture()
def client() -> Client:
    return TestClient(ms)


def _gen_valid_tasklist() -> TaskList:
    tasklist = TaskList()
    tasklist.id = 1
    tasklist.user_id = 1
    tasklist.user_email = "example@example.com"
    tasklist.title = "test tasklist"

    return tasklist


@pytest.fixture
def valid_tasklist() -> TaskList:
    return _gen_valid_tasklist()


@pytest.fixture
def valid_task() -> Task:
    task = Task()
    task.id = 1
    task.list_id = 1
    task.title = "test task"
    task.description = "test description"
    task.deadline = datetime.now()
    task.is_completed = False
    task.is_notified = False

    return task
