from datetime import datetime, timedelta
import typing

from cryptography.fernet import Fernet
from fastapi.responses import JSONResponse
from jose import jwt

from models import UserDB
from settings import USER_DB, SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRED
from schemas.auth import Payload, CustomResponse


f = Fernet(SECRET_KEY)


def encrypt_password(raw_password: str) -> str:
    encoded_password = raw_password.encode('utf-8')
    encrypted_password = f.encrypt(encoded_password).decode('utf-8')
    return encrypted_password


def decrypt_password(encrypted_password: str) -> str:
    return f.decrypt(encrypted_password).decode('utf-8')


def authenticate_user(username: str, password: str) -> typing.Union[UserDB, None]:
    response_data = USER_DB.fetch({'username': username})
    if response_data.count == 0:
        return None

    user = response_data.items[0]
    user_instance = UserDB(**user)

    if decrypt_password(user_instance.password) != password:
        return None

    return user_instance


def create_token(data: typing.Dict[str, typing.Any], expiration_delta: timedelta, offset_hours: int = 0) -> str:
    to_encode = data.copy()
    now = datetime.now()
    to_encode.update({
        'exp': now + expiration_delta + timedelta(hours=offset_hours),
        'iat': now
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_access_token(data: typing.Dict[str, typing.Any]) -> str:
    expiration_delta = timedelta(seconds=JWT_EXPIRED)
    offset_hours = -7
    return create_token(data, expiration_delta, offset_hours)


def create_refresh_token(data: typing.Dict[str, typing.Any]) -> str:
    expiration_delta = timedelta(days=30)
    return create_token(data, expiration_delta)


def get_payload_from_token(access_token: str) -> Payload:
    return Payload(**jwt.decode(access_token, SECRET_KEY, algorithms=[JWT_ALGORITHM]))


def create_response(
        message: str,
        success: bool = False,
        status_code: int = 400,
        data: typing.Union[typing.Dict[str, typing.Any], typing.List[typing.Any], None] = None
) -> JSONResponse:
    response = CustomResponse(
        success=success,
        code=status_code,
        message=message,
        data=data
    )
    return JSONResponse(
        response.dict(),
        status_code=status_code
    )



