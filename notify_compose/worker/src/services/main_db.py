from abc import ABC, abstractmethod
from typing import Any, Optional
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorDatabase


class AbstractMainStorage(ABC):
    @abstractmethod
    def create(self, collection: str, item: Any):
        pass

    @abstractmethod
    def get_all(self, collection: str):
        pass

    @abstractmethod
    def get_one(self, collection: str, uuid: UUID):
        pass

    @abstractmethod
    def delete(self, collection: str, uuid: UUID):
        pass

    @abstractmethod
    def find(self, collection: str, **kwargs):
        pass


class BaseMongoStorage(AbstractMainStorage):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create(self, collection: str, item: Any) -> str:
        await self.db.get_collection(collection).insert_one(item.dict())

        return item.id

    async def get_all(self, collection: str) -> list[dict]:
        return [item async for item in self.db.get_collection(collection).find()]

    async def get_one(self, collection: str, uuid: UUID):
        return await self.db.get_collection(collection).find_one({"id": uuid})

    async def delete(self, collection: str, uuid: UUID):
        await self.db.get_collection(collection).delete_one({"id": uuid})

    async def find(self, collection: str, **kwargs):
        return await self.db.get_collection(collection).find(**kwargs)


class MainStorage:
    def __init__(self, db: AbstractMainStorage):
        self.db = db

    async def create(self, collection: str, item: Any) -> Optional[str]:
        return await self.db.create(collection=collection, item=item)

    async def get_all(self, collection: str) -> list[dict]:
        return await self.db.get_all(collection=collection)

    async def get_one(self, collection: str, uuid: UUID):
        return await self.db.get_one(collection=collection, uuid=uuid)

    async def delete(self, collection: str, uuid: UUID):
        await self.db.delete(collection=collection, uuid=uuid)

    async def find(self, collection: str, **kwargs):
        return await self.db.find(collection=collection, **kwargs)
