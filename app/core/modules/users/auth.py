import jwt as jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from starlette.requests import Request

from app.core.modules.spending.models import User

http_bearer = HTTPBearer(auto_error=False)
SECRET_KEY = 'your-secret-key'


class AuthenticationFailed(HTTPException):

    def __init__(self, detail=None):
        status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(status_code=status_code, detail=detail)


def decode_token(token: str) -> dict:
    payload = jwt.decode(
        jwt=token,
        key=SECRET_KEY,
        verify=True,
        algorithms=['HS256'],
        options={
            'verify_exp': True,
        },
    )
    return payload


async def user_auth_check(request: Request, credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> User:
    if not credentials:
        raise AuthenticationFailed
    try:
        payload = decode_token(token=credentials.credentials)
    except Exception as e:
        raise AuthenticationFailed(str(e))

    user_id = payload["user_id"]
    user = await User.filter(user_id=user_id).first()

    if not user:
        raise AuthenticationFailed

    return user
