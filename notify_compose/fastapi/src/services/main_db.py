import uuid
from abc import ABC, abstractmethod
from typing import Any, Optional

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class AbstractMainStorage(ABC):
    @abstractmethod
    def create(self, collection: str, item: Any):
        pass

    @abstractmethod
    def update(self, collection: str, id: str, update_field: str, data: uuid.UUID):
        pass


class BaseMongoStorage(AbstractMainStorage):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create(self, collection: str, item: Any) -> str:
        new_item = await self.db.get_collection(collection).insert_one(item.dict())

        return str(new_item.inserted_id)

    async def update(self, collection: str, id: str, update_field: str, data: uuid.UUID) -> None:
        await self.db.get_collection(collection).update_one({"_id": ObjectId(id)},
                                                            {"$push": {update_field: data}})


class SecondaryStorage:
    def __init__(self, db: BaseMongoStorage):
        self.db = db

    async def create(self, collection: str, item: Any) -> Optional[str]:
        return await self.db.create(collection=collection, item=item)

    async def update(self, collection: str, id: str, update_field: str, data: uuid.UUID) -> None:
        await self.db.update(collection=collection, id=id, update_field=update_field, data=data)
