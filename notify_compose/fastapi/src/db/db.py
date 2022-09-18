from typing import Optional

from services.main_db import AbstractMainStorage

db: Optional[AbstractMainStorage] = None


# Функция понадобится при внедрении зависимостей
async def get_db() -> AbstractMainStorage:
    if not db:
        raise
    return db
