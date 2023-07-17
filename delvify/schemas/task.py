from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    is_completed: bool = False


class TasksMulti(BaseModel):
    tasks_id: List[int]


class TaskCreate(TaskBase):
    list_id: int


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    deadline: Optional[datetime]
    is_completed: bool


class TaskUpdateWithNotify(TaskUpdate):
    is_notified: bool


class Task(TaskCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
