from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from delvify import crud, schemas
from delvify.api.helpers import get_or_404
from delvify.core import di

endpoint = APIRouter()


@endpoint.post("", response_model=schemas.Task)
def create_task(
    *,
    form: schemas.TaskCreate,
    user_id: int = Depends(di.get_current_user_id),
) -> Any:
    get_or_404(crud.tasklist.get_by_id, id=form.list_id, user_id=user_id)
    if form.deadline is not None and form.deadline <= datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Deadline must be in the future")
    return crud.task.create(form=form)


@endpoint.get("/{id}", response_model=schemas.Task)
def get_task(
    id: int,
    user_id: int = Depends(di.get_current_user_id),
) -> Any:
    return get_or_404(crud.task.get_by_id, id=id, user_id=user_id)


@endpoint.put("/{id}", response_model=schemas.Task)
def update_task(
    id: int,
    form: schemas.TaskUpdate,
    user_id: int = Depends(di.get_current_user_id),
) -> Any:
    task = get_or_404(crud.task.get_by_id, id=id, user_id=user_id)
    if form.is_completed is not None and form.is_completed:
        notifier = di.get_notification_service()
        if notifier:
            notifier.send_email(
                schemas.Email(
                    destination=task.list.user_email,
                    subject="Your task was completed!",
                    body=f'Task "{task.title}" was completed! Congrats',
                )
            )
    if form.deadline is not None and form.deadline > datetime.now(timezone.utc):
        return crud.task.update_with_is_notified(
            id=id, task_update=form, is_notified=False
        )
    return crud.task.update(db_obj=task, form=form)


@endpoint.put("/parent/{new_list_id}", response_model=BaseModel)
def update_tasks_parent_list(
    new_list_id: int,
    form: schemas.TasksMulti,
    user_id: int = Depends(di.get_current_user_id),
) -> Any:
    get_or_404(crud.tasklist.get_by_id, id=new_list_id, user_id=user_id)
    tasks = get_or_404(crud.task.get_by_ids, ids=form.tasks_id, user_id=user_id)
    crud.task.update_parent(tasks=tasks, new_parent_id=new_list_id)
    return {}


@endpoint.delete("", response_model=BaseModel)
def delete_tasks(
    form: schemas.TasksMulti,
    user_id: int = Depends(di.get_current_user_id),
) -> Any:
    tasks = get_or_404(crud.task.get_by_ids, ids=form.tasks_id, user_id=user_id)
    crud.task.remove_multi(tasks=tasks)
    return {}
