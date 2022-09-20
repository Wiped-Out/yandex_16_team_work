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


class BaseMongoStorage(AbstractMainStorage):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create(self, collection: str, item: Any) -> str:
        new_item = await self.db.get_collection(collection).insert_one(item.dict())

        return str(new_item.inserted_id)

    async def get_all(self, collection: str) -> list[dict]:
        return [item async for item in self.db.get_collection(collection).find()]

    async def get_one(self, collection: str, uuid: UUID):
        return await self.db.get_collection(collection).find_one({"id": uuid})

    async def delete(self, collection: str, uuid: UUID):
        await self.db.get_collection(collection).delete_one({"id": uuid})


class MainStorage:
    def __init__(self, db: BaseMongoStorage):
        self.db = db

    async def create(self, collection: str, item: Any) -> Optional[str]:
        return await self.db.create(collection=collection, item=item)

    async def get_all(self, collection: str) -> list[dict]:
        return await self.db.get_all(collection=collection)

    async def get_one(self, collection: str, uuid: UUID):
        return await self.db.get_one(collection=collection, uuid=uuid)

    async def delete(self, collection: str, uuid: UUID):
        await self.db.delete(collection=collection, uuid=uuid)
