from typing import Optional

from services.db import AbstractStorage

db: Optional[AbstractStorage] = None


# Функция понадобится при внедрении зависимостей
async def get_db() -> AbstractStorage:
    if not db:
        raise
    return db
