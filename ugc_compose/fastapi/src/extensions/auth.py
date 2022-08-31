import uuid

from core.config import settings
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.auth import AuthUser
from services.auth_integration import get_auth_service


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, auth_service=Depends(get_auth_service)) -> AuthUser:  # type: ignore
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)  # type: ignore
        if settings.NO_JWT:
            return AuthUser(highest_role=0, uuid=uuid.uuid4())
        if credentials:
            if credentials.scheme != 'Bearer':
                raise HTTPException(status_code=403, detail='Invalid authentication scheme.')
            return await auth_service.auth_user(credentials.credentials)


security = JWTBearer()
