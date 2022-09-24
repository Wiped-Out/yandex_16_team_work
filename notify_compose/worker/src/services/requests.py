from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import aiohttp
from multidict import CIMultiDictProxy


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


class AIOHTTPManager:
    """Контекстный менеджер для работы с AIOHTTP"""

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def __aenter__(self) -> aiohttp.ClientSession:
        return self.session

    async def __aexit__(self, error: Exception, value: object, traceback: object):  # noqa: WPS110
        await self.session.close()


class AsyncRequest(ABC):
    @abstractmethod
    async def get(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        pass  # noqa: WPS420

    @abstractmethod
    async def post(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        pass  # noqa: WPS420

    @abstractmethod
    async def delete(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        pass  # noqa: WPS420

    @abstractmethod
    async def put(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        pass  # noqa: WPS420

    @abstractmethod
    async def patch(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        pass  # noqa: WPS420


class AIOHTTPClient(AsyncRequest):
    async def get(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        async with AIOHTTPManager() as session:
            async with session.get(url, params=query, json=body, headers=headers) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    async def post(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        async with AIOHTTPManager() as session:
            async with session.post(url, params=query, json=body, headers=headers) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    async def delete(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        async with AIOHTTPManager() as session:
            async with session.delete(url, params=query, json=body, headers=headers) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    async def put(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        async with AIOHTTPManager() as session:
            async with session.put(url, params=query, json=body, headers=headers) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    async def patch(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        async with AIOHTTPManager() as session:
            async with session.patch(url, params=query, json=body, headers=headers) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )


class BaseRequest:
    client: AsyncRequest = AIOHTTPClient()

    async def get(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        return await self.client.get(
            url=url,
            body=body,
            query=query,
            headers=headers,
            **kwargs,
        )

    async def post(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        return await self.client.post(
            url=url,
            body=body,
            query=query,
            headers=headers,
            **kwargs,
        )

    async def delete(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        return await self.client.delete(
            url=url,
            body=body,
            query=query,
            headers=headers,
            **kwargs,
        )

    async def put(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        return await self.client.put(
            url=url,
            body=body,
            query=query,
            headers=headers,
            **kwargs,
        )

    async def patch(  # noqa: WPS211
            self,
            url: str,
            body: Optional[dict] = None,
            query: Optional[dict] = None,
            headers: Optional[dict] = None,
            **kwargs,
    ):
        return await self.client.patch(
            url=url,
            body=body,
            query=query,
            headers=headers,
            **kwargs,
        )
