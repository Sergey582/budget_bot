import hashlib
import hmac

from app.core.config import BOT_TOKEN
from app.core.modules.spending.models import User
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request


class Credentials(BaseModel):
    data_check_string: str
    received_hash: str
    telegram_user_id: int


class AuthenticationFailed(HTTPException):

    def __init__(self, detail=None):
        status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(status_code=status_code, detail=detail)


def verify_telegram_data(data_check_string: str, received_hash: str) -> bool:
    secret_key = hashlib.sha256(BOT_TOKEN.encode('utf-8'))
    message = data_check_string.encode('utf-8')
    generated_hash = hmac.new(secret_key.digest(), message, hashlib.sha256).hexdigest()
    return generated_hash == received_hash


async def user_auth_check(request: Request, credentials: Credentials = Depends()) -> User:
    if not credentials:
        raise AuthenticationFailed

    if not verify_telegram_data(
            data_check_string=credentials.data_check_string,
            received_hash=credentials.received_hash,
    ):
        raise AuthenticationFailed("invalid credentials")

    user_id = credentials.telegram_user_id
    user = await User.filter(user_id=user_id).first()

    if user is None:
        user = User(user_id=user_id)
        await user.save()

    return user
