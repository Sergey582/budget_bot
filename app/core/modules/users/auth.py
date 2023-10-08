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


def verify_telegram_data(data_check_string: str, received_hash: str):
    # Calculate the HMAC-SHA256 hash
    calculated_hash = hmac.new(BOT_TOKEN.encode(), data_check_string.encode(), hashlib.sha256).hexdigest()

    # Compare the calculated hash with the received hash
    if calculated_hash == received_hash:
        return True
    else:
        return False


async def user_auth_check(request: Request, credentials: Credentials = Depends()) -> User:
    if not credentials:
        raise AuthenticationFailed

    # if not verify_telegram_data(
    #         data_check_string=credentials.data_check_string,
    #         received_hash=credentials.received_hash,
    # ):
    #     raise AuthenticationFailed("invalid credentials")
    #
    user_id = credentials.telegram_user_id
    user = await User.filter(user_id=user_id).first()

    if not user:
        raise AuthenticationFailed("user not found")

    return user
