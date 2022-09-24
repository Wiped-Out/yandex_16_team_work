from functools import lru_cache
from typing import Optional

from db.db import get_db
from fastapi import Depends
from models.models import AddTemplate, Template
from pydantic import UUID4
from services.main_db import AbstractMainStorage, MainStorage


class TemplatesService(MainStorage):
    collection: str = 'templates'

    async def add_template(self, template: AddTemplate):
        return await self.create(
            collection=self.collection,
            item=Template(**template.dict()),
        )

    async def get_templates(self) -> list[Template]:
        items: list[dict] = await self.get_all(collection=self.collection)
        return [Template(**item) for item in items]

    async def get_template(self, template_id: UUID4) -> Optional[Template]:
        item = await self.get_one(collection=self.collection, uuid=template_id)
        if not item:
            return None
        return Template(**item)

    async def delete_template(self, template_id: UUID4):
        return await self.delete(collection=self.collection, uuid=template_id)


@lru_cache()
def get_templates_service(
        db: AbstractMainStorage = Depends(get_db),
) -> TemplatesService:
    return TemplatesService(db=db)
