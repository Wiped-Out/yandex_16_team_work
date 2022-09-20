from functools import lru_cache
from models.models import Template
from typing import Optional


class TemplatesService:
    async def get_templates(self) -> list[Template]:
        # todo
        pass

    async def get_template(self, template_id: str) -> Optional[Template]:
        # todo
        pass

    async def delete_template(self, template_id: str):
        # todo
        pass


@lru_cache()
def get_templates_service() -> TemplatesService:
    return TemplatesService()
