from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import aiohttp
from multidict import CIMultiDictProxy

from utils.utils import backoff


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


class AIOHTTPManager:
    """Контекстный менеджер для работы с AIOHTTP"""

    async def get_session(self):
        self.session = aiohttp.ClientSession()

    async def __aenter__(self) -> aiohttp.ClientSession:
        await self.get_session()
        return self.session

    async def __aexit__(self, error: Exception, value: object, traceback: object):
        await self.session.close()


class AsyncRequest(ABC):
    @abstractmethod
    async def get(self,
                  url: str,
                  body: Optional[dict] = None,
                  query: Optional[dict] = None,
                  headers: Optional[dict] = None,
                  **kwargs):
        pass

    @abstractmethod
    async def post(self,
                   url: str,
                   body: Optional[dict] = None,
                   query: Optional[dict] = None,
                   headers: Optional[dict] = None,
                   **kwargs):
        pass

    @abstractmethod
    async def delete(self,
                     url: str,
                     body: Optional[dict] = None,
                     query: Optional[dict] = None,
                     headers: Optional[dict] = None,
                     **kwargs):
        pass

    @abstractmethod
    async def put(self,
                  url: str,
                  body: Optional[dict] = None,
                  query: Optional[dict] = None,
                  headers: Optional[dict] = None,
                  **kwargs):
        pass

    @abstractmethod
    async def patch(self,
                    url: str,
                    body: Optional[dict] = None,
                    query: Optional[dict] = None,
                    headers: Optional[dict] = None,
                    **kwargs):
        pass


class AIOHTTPClient(AsyncRequest):
    @backoff(factor=11, border_sleep_time=1)
    async def get(self,
                  url: str,
                  body: Optional[dict] = None,
                  query: Optional[dict] = None,
                  headers: Optional[dict] = None,
                  **kwargs):
        async with AIOHTTPManager() as session:
            async with session.get(url, params=query, json=body, headers=headers) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    async def post(self,
                   url: str,
                   body: Optional[dict] = None,
                   query: Optional[dict] = None,
                   headers: Optional[dict] = None,
                   **kwargs):
        async with AIOHTTPManager() as session:
            async with session.post(url, params=query, json=body, headers=headers) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    async def delete(self,
                     url: str,
                     body: Optional[dict] = None,
                     query: Optional[dict] = None,
                     headers: Optional[dict] = None,
                     **kwargs):
        async with AIOHTTPManager() as session:
            async with session.delete(url, params=query, json=body, headers=headers) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    async def put(self,
                  url: str,
                  body: Optional[dict] = None,
                  query: Optional[dict] = None,
                  headers: Optional[dict] = None,
                  **kwargs):
        async with AIOHTTPManager() as session:
            async with session.put(url, params=query, json=body, headers=headers) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    async def patch(self,
                    url: str,
                    body: Optional[dict] = None,
                    query: Optional[dict] = None,
                    headers: Optional[dict] = None,
                    **kwargs):
        async with AIOHTTPManager() as session:
            async with session.patch(url, params=query, json=body, headers=headers) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )


class BaseRequest:
    client = AIOHTTPClient()

    async def get(self,
                  url: str,
                  body: Optional[dict] = None,
                  query: Optional[dict] = None,
                  headers: Optional[dict] = None,
                  **kwargs):
        return await self.client.get(url=url,
                               body=body,
                               query=query,
                               headers=headers,
                               **kwargs)

    async def post(self,
                   url: str,
                   body: Optional[dict] = None,
                   query: Optional[dict] = None,
                   headers: Optional[dict] = None,
                   **kwargs):
        return await self.client.post(url=url,
                                body=body,
                                query=query,
                                headers=headers,
                                **kwargs)

    async def delete(self,
                     url: str,
                     body: Optional[dict] = None,
                     query: Optional[dict] = None,
                     headers: Optional[dict] = None,
                     **kwargs):
        return await self.client.delete(url=url,
                                  body=body,
                                  query=query,
                                  headers=headers,
                                  **kwargs)

    async def put(self,
                  url: str,
                  body: Optional[dict] = None,
                  query: Optional[dict] = None,
                  headers: Optional[dict] = None,
                  **kwargs):
        return await self.client.put(url=url,
                               body=body,
                               query=query,
                               headers=headers,
                               **kwargs)

    async def patch(self,
                    url: str,
                    body: Optional[dict] = None,
                    query: Optional[dict] = None,
                    headers: Optional[dict] = None,
                    **kwargs):
        return await self.client.patch(url=url,
                                 body=body,
                                 query=query,
                                 headers=headers,
                                 **kwargs)
