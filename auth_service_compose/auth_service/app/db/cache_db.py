from typing import Optional

from services.base_cache import CacheStorage

cache: Optional[CacheStorage] = None


def get_cache_db() -> CacheStorage:
    return cache
