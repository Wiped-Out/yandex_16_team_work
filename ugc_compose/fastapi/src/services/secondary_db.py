import uuid
from abc import ABC, abstractmethod
from typing import Any, Optional

from bson.objectid import ObjectId
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorDatabase


class AbstractSecondaryStorage(ABC):
    @abstractmethod
    def create(self, collection: str, item: Any):
        pass

    @abstractmethod
    def update(self, collection: str, id: str, update_field: str, data: uuid.UUID):
        pass


class BaseMongoStorage(AbstractSecondaryStorage):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create(self, collection: str, item: Any) -> Optional[str]:
        try:
            new_item = await self.db.get_collection(collection).insert_one(item.dict())
        except Exception as e:
            logger.error(e)
        else:
            logger.info(
                await self.db.get_collection(collection).find_one({"_id": new_item.inserted_id})
            )
            return str(new_item.inserted_id)
        return None

    async def update(self, collection: str, id: str, update_field: str, data: uuid.UUID) -> None:
        try:
            await self.db.get_collection(collection).update_one(
                {"_id": ObjectId(id)},
                {"$push": {update_field: data}}
            )
        except Exception as e:
            logger.error(e)
        logger.info(await self.db.get_collection(collection).find_one({"_id": ObjectId(id)}))


class SecondaryStorage:
    def __init__(self, db: BaseMongoStorage):
        self.db = db

    async def create(self, collection: str, item: Any) -> Optional[str]:
        return await self.db.create(collection=collection, item=item)

    async def update(self, collection: str, id: str, update_field: str, data: uuid.UUID) -> None:
        await self.db.update(collection=collection, id=id, update_field=update_field, data=data)
