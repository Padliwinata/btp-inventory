from datetime import datetime, timedelta
import typing

from cryptography.fernet import Fernet
from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from db import db_users
from exceptions import DependencyException
from models import UserDB
from settings import SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRED
from schemas.auth import Payload, CustomResponse


f = Fernet(SECRET_KEY)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/auth/login', auto_error=False)


def encrypt_password(raw_password: str) -> str:
    encoded_password = raw_password.encode('utf-8')
    encrypted_password = f.encrypt(encoded_password).decode('utf-8')
    return encrypted_password


def decrypt_password(encrypted_password: str) -> str:
    return f.decrypt(encrypted_password).decode('utf-8')


def authenticate_user(username: str, password: str) -> typing.Union[UserDB, None]:
    response_data = db_user.fetch({'username': username})
    if response_data.count == 0:
        return None

    user = response_data.items[0]
    user_instance = UserDB(**user)

    if decrypt_password(user_instance.password) != password:
        return None

    return user_instance


def create_token(username: str, expiration_delta: timedelta, offset_hours: int = 0) -> str:
    to_encode = {'sub': username}
    now = datetime.now()
    to_encode.update({
        'exp': now + expiration_delta + timedelta(hours=offset_hours),
        'iat': now
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_access_token(username: str) -> str:
    expiration_delta = timedelta(seconds=JWT_EXPIRED)
    offset_hours = -7
    return create_token(username, expiration_delta, offset_hours)


def create_refresh_token(username: str) -> str:
    expiration_delta = timedelta(days=30)
    return create_token(username, expiration_delta)


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


def get_user(access_token: str = Depends(oauth2_scheme)) -> typing.Union[UserDB, None]:
    if not access_token:
        response_error = CustomResponse(
            success=False,
            code=status.HTTP_401_BAD_REQUEST,
            message="Authorization token not found",
            data=None
        )
        raise DependencyException(status_code=status.HTTP_401_UNAUTHORIZED, detail_info=response_error.dict())
    try:
        payload = get_payload_from_token(access_token)
    except JWTError:
        response_error = CustomResponse(
            success=False,
            code=status.HTTP_401_UNAUTHORIZED,
            message="Authorization token is invalid",
            data=None
        )
        raise DependencyException(status_code=status.HTTP_401_UNAUTHORIZED, detail_info=response_error.dict())

    response_data = db_user.fetch({'username': payload.sub})
    if response_data.count == 0:
        response_error = CustomResponse(
            success=False,
            code=status.HTTP_401_BAD_REQUEST,
            message="Authorization token subject is not found",
            data=None
        )
        raise DependencyException(status_code=status.HTTP_401_UNAUTHORIZED, detail_info=response_error.dict())

    user_data = response_data.items[0]
    return UserDB(**user_data)






