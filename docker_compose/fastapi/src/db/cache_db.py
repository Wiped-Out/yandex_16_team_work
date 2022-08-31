from typing import Optional

from services.base_cache import AsyncCacheStorage

cache: Optional[AsyncCacheStorage] = None


# Функция понадобится при внедрении зависимостей
async def get_cache_db() -> AsyncCacheStorage:
    if not cache:
        raise
    return cache
