from abc import ABC, abstractmethod
from typing import Optional

from elasticsearch import AsyncElasticsearch
from elasticsearch import NotFoundError


class AsyncFullTextSearchStorage(ABC):
    @abstractmethod
    async def get(self, index: str, id: str, **kwargs):
        pass

    @abstractmethod
    async def search(
            self,
            index: str,
            body: dict,
            from_: Optional[int] = None,
            size: Optional[int] = None,
            **kwargs
    ):
        pass

    @abstractmethod
    async def count(self, index: str, body: Optional[dict] = None, **kwargs):
        pass


class BaseElasticStorage(AsyncFullTextSearchStorage):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get(self, index: str, id: str, **kwargs):
        return await self.elastic.get(index=index, id=id)

    async def search(
            self,
            index: str,
            body: dict,
            from_: Optional[int] = None,
            size: Optional[int] = None,
            **kwargs
    ):
        return await self.elastic.search(index=index, body=body, from_=from_, size=size)

    async def count(self, index: str, body: Optional[dict] = None, **kwargs):
        return await self.elastic.count(index=index, body=body)


class BaseFullTextSearchStorage:
    def __init__(self, full_text_search: AsyncFullTextSearchStorage, **kwargs):
        super().__init__(**kwargs)

        self.full_text_search = full_text_search

    async def get_by_id(
            self,
            _id: str,
            model,
            index: str
    ):
        try:
            doc = await self.full_text_search.get(index, _id)
        except NotFoundError:
            return None

        return model(**doc["_source"])

    async def get_data(
            self,
            page: int,
            page_size: int,
            model,
            index: str,
    ):
        query = {
            "query": {
                "match_all": {}
            }
        }

        try:
            doc = await self.full_text_search.search(
                index=index,
                body=query,
                from_=page_size * (page - 1),
                size=page_size,
            )
            return [model(**item["_source"]) for item in doc["hits"]["hits"]]
        except NotFoundError:
            return []

    async def count_all_data_in_index(self, index: str) -> int:
        count = await self.full_text_search.count(index=index)
        return count["count"]

    async def search(
            self,
            search: str,
            fields: list[str],
            index: str,
            page: int,
            page_size: int,
    ) -> dict:
        query = {
            "query": {
                "multi_match": {
                    "query": search,
                    "fields": fields,
                    "fuzziness": "auto"
                }
            }
        }

        try:
            doc = await self.full_text_search.search(
                index=index,
                body=query,
                from_=page_size * (page - 1),
                size=page_size
            )
        except NotFoundError:
            return {}

        return doc

    async def get_items_by_search(
            self,
            search: str,
            fields: list[str],
            index: str,
            model,
            page: int,
            page_size: int
    ) -> list:
        doc = await self.search(
            search=search,
            fields=fields,
            index=index,
            page=page,
            page_size=page_size
        )

        if not doc:
            return []

        return [model(**item["_source"]) for item in doc["hits"]["hits"]]
