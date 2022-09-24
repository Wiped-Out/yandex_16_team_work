from typing import Optional

from services.queue import AbstractQueue

queue: Optional[AbstractQueue] = None


def get_queue() -> AbstractQueue:
    return queue
