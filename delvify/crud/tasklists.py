from typing import List, Optional

from sqlalchemy.orm import Query, joinedload

from delvify.core import di
from delvify.crud import CRUDBase
from delvify.models import TaskList
from delvify.schemas import TaskListCreate, TaskListUpdate


class CRUDList(CRUDBase[TaskList, TaskListCreate, TaskListUpdate]):
    def get_by_id(self, id: int, user_id: int) -> Optional[TaskList]:
        return self._get_lists_with_tasks(user_id).filter(TaskList.id == id).first()

    def get_by_title(self, *, title: str, user_id: int) -> Optional[TaskList]:
        return (
            self._get_lists_with_tasks(user_id).filter(TaskList.title == title).first()
        )

    def get_by_user_id(self, *, user_id: int) -> List[TaskList]:
        return self._get_lists_with_tasks(user_id).all()

    def _get_lists_with_tasks(self, user_id: int) -> Query:
        return (
            self._db.query(TaskList)
            .options(joinedload(TaskList.tasks))
            .filter(TaskList.user_id == user_id)
        )


tasklist = CRUDList(db=di.get_db(), model=TaskList)
