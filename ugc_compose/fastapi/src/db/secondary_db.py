from typing import Optional

from services.secondary_db import AbstractSecondaryStorage

db: Optional[AbstractSecondaryStorage] = None


# Функция понадобится при внедрении зависимостей
async def get_db() -> AbstractSecondaryStorage:
    if not db:
        raise
    return db
