import time
from typing import Callable, Optional

import schedule

from delvify.core import logger
from delvify.jobs import Job, get_deadline_notification_job


def register_minutely_job(
    create_job: Callable[..., Optional[Job]],
    interval: int,
):
    logger.info(
        f"Registering minutely job {create_job.__name__} to run every {interval} minutes"
    )
    maybe_job = create_job()
    if maybe_job:
        schedule.every(interval).minutes.do(maybe_job.run)
    else:
        logger.error(f"Job {create_job.__name__} was not created properly. Skipping.")


if __name__ == "__main__":
    register_minutely_job(get_deadline_notification_job, interval=10)

    while True:
        schedule.run_pending()
        time.sleep(1)
