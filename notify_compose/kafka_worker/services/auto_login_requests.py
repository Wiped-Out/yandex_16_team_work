from functools import wraps

from services.requests import BaseRequest


class AuthorizationError(Exception):
    pass


def auto_authorize():
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            self = args[0]
            headers = kwargs.get('headers', dict())
            headers['Authorization'] = f'Bearer {self.user["TOKEN"]}'
            kwargs['headers'] = headers
            response = await func(*args, **kwargs)
            if response.status >= 400:
                response = await self.client.post(
                    url=self.user["REFRESH_URL"],
                    headers={'Authorization': f'Bearer {self.user["REFRESH_TOKEN"]}'},
                )
                if response.status < 300:
                    self.user["TOKEN"] = response.body['access_token']
                else:
                    raise AuthorizationError('Authorization failed')

                kwargs['headers']['Authorization'] = f'Bearer {self.user["TOKEN"]}'
                response = await func(*args, **kwargs)
            return response

        return inner

    return func_wrapper


class AutoLoginRequests(BaseRequest):
    def __init__(self, user: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    @auto_authorize()
    async def get(self, *args, **kwargs):
        return await super().get(*args, **kwargs)

    @auto_authorize()
    async def post(self, *args, **kwargs):
        return await super().post(*args, **kwargs)

    @auto_authorize()
    async def delete(self, *args, **kwargs):
        return await super().delete(*args, **kwargs)

    @auto_authorize()
    async def put(self, *args, **kwargs):
        return await super().put(*args, **kwargs)

    @auto_authorize()
    async def patch(self, *args, **kwargs):
        return await super().patch(*args, **kwargs)
