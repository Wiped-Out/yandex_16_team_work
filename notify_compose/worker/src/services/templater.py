from abc import ABC, abstractmethod

from jinja2 import BaseLoader, Environment
from models.models import Template


class AbstractTemplater(ABC):
    @staticmethod
    @abstractmethod
    async def render(item: Template, data: dict):
        pass


class Templater(AbstractTemplater):
    @staticmethod
    async def render(item: Template, data: dict) -> str:
        template = Environment(loader=BaseLoader, enable_async=True).from_string(item.body)
        return await template.render_async(**data)
