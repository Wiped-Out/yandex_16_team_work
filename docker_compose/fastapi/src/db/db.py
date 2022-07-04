from typing import Optional

from services.base_full_text_search import AsyncFullTextSearchStorage

full_text_search: Optional[AsyncFullTextSearchStorage] = None


# Функция понадобится при внедрении зависимостей
async def get_db() -> AsyncFullTextSearchStorage:
    return full_text_search
