from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import and_, false

from delvify.core import di
from delvify.crud import CRUDBase
from delvify.models import Task, TaskList
from delvify.schemas import TaskCreate
from delvify.schemas.task import TaskUpdate, TaskUpdateWithNotify


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def get_by_id(self, id: int, user_id: int) -> Optional[Task]:
        maybe_task = self._db.query(Task).filter(Task.id == id).first()
        if maybe_task is None or maybe_task.list.user_id != user_id:
            return None
        return maybe_task

    def get_by_ids(self, ids: List[int], user_id: int) -> Optional[List[Task]]:
        tasks = (
            self._db.query(Task)
            .join(Task.list)
            .filter(Task.id.in_(ids), TaskList.user_id == user_id)
            .options(joinedload(Task.list))
            .all()
        )
        if len(tasks) != len(ids):
            return None
        return tasks

    def get_by_deadline_between(self, *, lo: datetime, hi: datetime) -> List[Task]:
        return (
            self._db.query(Task)
            .filter(Task.is_completed == false())
            .filter(and_(Task.deadline > lo, Task.deadline < hi))
            .all()
        )

    def update_parent(self, *, tasks: List[Task], new_parent_id: int) -> int:
        n_updated = (
            self._db.query(Task)
            .filter(Task.id.in_(map(lambda t: t.id, tasks)))
            .update({"list_id": new_parent_id}, synchronize_session=False)
        )
        self._db.commit()
        return n_updated

    def update_with_is_notified(
        self, id: int, task_update: TaskUpdate, is_notified: bool
    ) -> Optional[Task]:
        task_from_db = self._db.query(Task).filter(Task.id == id).first()

        if task_from_db is None:
            return None

        update_schema = TaskUpdateWithNotify(
            **task_update.model_dump(exclude_unset=True), is_notified=is_notified
        )

        return self.update(db_obj=task_from_db, form=update_schema)

    def remove_multi(self, *, tasks: List[Task]) -> int:
        n_deleted = (
            self._db.query(Task)
            .filter(Task.id.in_(map(lambda t: t.id, tasks)))
            .delete(synchronize_session=False)
        )
        self._db.commit()
        return n_deleted


task = CRUDTask(db=di.get_db(), model=Task)
