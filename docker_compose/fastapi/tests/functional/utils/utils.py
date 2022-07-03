import time
from functools import wraps


def backoff(
        start_sleep_tie: float = 0.1, factor: int = 2,
        border_sleep_time: int = 10,
):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            power: int = 0

            try:
                return func(*args, **kwargs)
            except Exception:
                t = start_sleep_tie * (factor ** power)
                if t >= border_sleep_time:
                    t = border_sleep_time

                time.sleep(t)
                power += 1

        return inner

    return func_wrapper
