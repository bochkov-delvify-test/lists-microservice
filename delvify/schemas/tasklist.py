from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr

from .task import Task


class TaskListBase(BaseModel):
    title: str


class TaskListCreateInternal(TaskListBase):
    user_email: EmailStr


class TaskListCreate(TaskListCreateInternal):
    user_id: int


class TaskListUpdate(TaskListBase):
    pass


class TaskList(TaskListBase):
    id: int
    tasks: List[Task] = []

    model_config = ConfigDict(from_attributes=True)
