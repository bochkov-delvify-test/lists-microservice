from datetime import datetime, timedelta
from itertools import groupby
from typing import Optional

from delvify import crud
from delvify.core import logger
from delvify.core.di import get_notification_service
from delvify.jobs.job import Job
from delvify.schemas import Email, TaskUpdate
from delvify.services.notification import NotificationService


class DeadlineNotificationJob(Job):
    def __init__(self, notifier: NotificationService):
        super().__init__()
        self._notifier = notifier

    def _do_run(self):
        yesterday = datetime.utcnow() - timedelta(
            days=1
        )  # We don't want to send notifications for tasks that were due later than yesterday
        now = datetime.utcnow()
        tasks = crud.task.get_by_deadline_between(lo=yesterday, hi=now)
        filtered_tasks = [
            task
            for task in tasks
            if task.is_notified is not None and not task.is_notified
        ]

        grouped = groupby(filtered_tasks, lambda t: t.list.user_email)

        self.log.info(
            f"Found {len(filtered_tasks)} tasks with deadline between {yesterday} and {now}"
        )

        for email, group in grouped:
            try:
                self._notifier.send_email(
                    Email(
                        destination=email,
                        subject="Deadline for some of your tasks is coming soon!",
                        body="\n".join(group.title for group in group),
                    )
                )
            except Exception as e:
                self.log.exception(f"Failed to send email to {email}", exc_info=e)
                continue
            for task in group:
                crud.task.update_with_is_notified(
                    id=task.id,
                    task_update=TaskUpdate(
                        title=task.title,
                        description=task.description,
                        deadline=task.deadline,
                        is_completed=task.is_completed,
                    ),
                    is_notified=True,
                )


def get_deadline_notification_job() -> Optional[DeadlineNotificationJob]:
    notifier = get_notification_service()
    if notifier is None:
        logger.warning(
            "Notification service not configured, skipping deadline notification job"
        )
        return None
    return DeadlineNotificationJob(notifier)
