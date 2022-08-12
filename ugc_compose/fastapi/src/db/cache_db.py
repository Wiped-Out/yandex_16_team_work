from typing import Optional

cache: Optional[None] = None


# Функция понадобится при внедрении зависимостей
async def get_cache_db() -> None:
    return cache
