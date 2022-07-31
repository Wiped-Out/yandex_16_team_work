import uuid

import jwt
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.config import settings
from models.auth import AuthUser
from services.auth_integration import get_auth_service


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, auth_service=Depends(get_auth_service)):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if settings.NO_JWT:
            return AuthUser(highest_role=0, uuid=uuid.uuid4())
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            return await auth_service.auth_user(credentials.credentials)


security = JWTBearer()
