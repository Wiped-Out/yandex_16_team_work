from typing import Optional

db: Optional[None] = None


# Функция понадобится при внедрении зависимостей
async def get_db() -> None:
    return db
