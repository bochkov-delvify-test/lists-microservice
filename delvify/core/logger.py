import logging


class LoggerMixin:
    def __init__(self):
        logging.basicConfig(
            format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d:%(funcName)s: %(message)s",
            level=logging.INFO,
        )

    @property
    def log(self):
        return logging


logger = LoggerMixin().log
