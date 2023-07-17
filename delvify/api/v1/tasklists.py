from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from delvify import crud, schemas
from delvify.api.helpers import get_or_404
from delvify.core import di

endpoint = APIRouter()


@endpoint.post("", response_model=schemas.TaskList)
def create_tasklist(
    *,
    form: schemas.TaskListCreateInternal,
    user_id: int = Depends(di.get_current_user_id),
) -> Any:
    maybe_tasklist = crud.tasklist.get_by_title(title=form.title, user_id=user_id)
    if maybe_tasklist:
        raise HTTPException(
            status_code=400, detail="The list with this title already exists."
        )
    return crud.tasklist.create(
        form=schemas.TaskListCreate(
            title=form.title, user_id=user_id, user_email=form.user_email
        )
    )


@endpoint.get("", response_model=List[schemas.TaskList])
def get_all_tasklists(
    user_id: int = Depends(di.get_current_user_id),
) -> Any:
    user_tasklists = crud.tasklist.get_by_user_id(user_id=user_id)
    return user_tasklists


@endpoint.get("/{id}", response_model=schemas.TaskList)
def get_tasklist(
    id: int,
    user_id: int = Depends(di.get_current_user_id),
) -> Any:
    return get_or_404(crud.tasklist.get_by_id, id=id, user_id=user_id)


@endpoint.put("/{id}", response_model=schemas.TaskList)
def update_tasklist(
    id: int,
    form: schemas.TaskListUpdate,
    user_id: int = Depends(di.get_current_user_id),
) -> Any:
    tasklist = get_or_404(crud.tasklist.get_by_id, id=id, user_id=user_id)
    return crud.tasklist.update(db_obj=tasklist, form=form)


@endpoint.delete("/{id}", response_model=BaseModel)
def delete_tasklist(
    id: int,
    user_id: int = Depends(di.get_current_user_id),
) -> Any:
    get_or_404(crud.tasklist.get_by_id, id=id, user_id=user_id)
    crud.tasklist.remove(id=id)
    return {}
