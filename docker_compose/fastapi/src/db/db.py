from typing import Optional
from elasticsearch import AsyncElasticsearch

full_text_search: Optional[AsyncElasticsearch] = None


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> AsyncElasticsearch:
    return full_text_search
