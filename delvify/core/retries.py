import functools
import time

from delvify.core import logger


def retry(max_retries=5, base_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == max_retries - 1:
                        logger.exception(
                            f"Failed to execute {func.__name__}", exc_info=e
                        )
                        raise e
                    else:
                        delay = base_delay * (2**i)
                        time.sleep(delay)

        return wrapper

    return decorator
