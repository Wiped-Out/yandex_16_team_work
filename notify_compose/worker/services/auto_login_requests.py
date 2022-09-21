from functools import wraps

from notify_compose.worker.core.settings import JWTBearerUser, user
from notify_compose.worker.services.requests import AsyncRequest, AIOHTTPClient, BaseRequest


class AuthorizationError(Exception):
    pass


def auto_authorize(user: JWTBearerUser, async_client: AsyncRequest = AIOHTTPClient()):
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            kwargs['headers']['Authorization'] = f'Bearer {user.TOKEN}'
            result = await func(*args, **kwargs)
            if result.status_code == 401:
                result = await async_client.post(url=user.REFRESH_URL,
                                                 headers={'Authorization': f"Bearer {user.REFRESH_TOKEN}"})

                if result.status_code == 200:
                    user.TOKEN = result.body['token']
                else:
                    raise AuthorizationError('Authorization failed')

                kwargs['headers']['Authorization'] = f'Bearer {user.TOKEN}'
                result = await func(*args, **kwargs)
            return result

        return inner

    return func_wrapper


class AutoLoginRequests(BaseRequest):
    @auto_authorize(user=user)
    async def get(self, *args, **kwargs):
        return await super().get(*args, **kwargs)

    @auto_authorize(user=user)
    async def post(self, *args, **kwargs):
        return await super().post(*args, **kwargs)

    @auto_authorize(user=user)
    async def delete(self, *args, **kwargs):
        return await super().delete(*args, **kwargs)

    @auto_authorize(user=user)
    async def put(self, *args, **kwargs):
        return await super().put(*args, **kwargs)

    @auto_authorize(user=user)
    async def patch(self, *args, **kwargs):
        return await super().patch(*args, **kwargs)
