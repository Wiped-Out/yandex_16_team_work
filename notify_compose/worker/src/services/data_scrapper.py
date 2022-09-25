from abc import ABC, abstractmethod
from typing import Optional

from models.models import TemplateFieldItem
from utils.utils import fetch_result, replace_in_json

from services.auto_login_requests import AutoLoginRequests


class AbstractAsyncScrapper(ABC):
    @abstractmethod
    async def scrape(self, item: TemplateFieldItem):
        pass

    @abstractmethod
    async def get_result(self):
        pass


class AsyncScrapper(AbstractAsyncScrapper, AutoLoginRequests):
    def __init__(self, items: list[TemplateFieldItem], ready_data: Optional[dict] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items: list[TemplateFieldItem] = items
        self.ready_data: dict = ready_data if ready_data is not None else dict()

    async def scrape(self, item: TemplateFieldItem) -> TemplateFieldItem:
        item = TemplateFieldItem(**(await replace_in_json(item=item.dict(),
                                                          pattern=',start,(.*?),end,',
                                                          replace_from=self.ready_data)))
        method = getattr(self, item.http_type)
        response = await method(url=item.url, body=item.body, headers=item.headers)
        fetched_result = fetch_result(body=response.body, pattern=item.fetch_pattern)
        self.ready_data[item.name] = fetched_result
        return item

    async def get_result(self) -> dict:
        for i in range(len(self.items)):
            self.items[i] = await self.scrape(item=self.items[i])
        return self.ready_data
