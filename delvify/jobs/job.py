from abc import ABC, abstractmethod
from typing import final

from delvify.core.logger import LoggerMixin


class Job(ABC, LoggerMixin):  # monitoring, alerting
    @final
    def run(self, *args, **kwargs):
        self.log.info(f"Running job {self.__class__.__name__}")
        try:
            self._do_run(*args, **kwargs)
            self.log.info(f"Job {self.__class__.__name__} completed successfully")
        except Exception as e:
            self.log.error(f"Job {self.__class__.__name__} failed with error {e}")

    @abstractmethod
    def _do_run(self, *args, **kwargs):
        raise NotImplementedError
