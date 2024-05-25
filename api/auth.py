from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from base import router
from db import *
from dependencies import create_response, encrypt_password, decrypt_password, create_refresh_token, create_access_token
from schemas.auth import RegisterForm, TokenResponse


@router.post('/register', tags=['Auth'])
async def register(form: RegisterForm) -> JSONResponse:
    response_data = db_user.fetch([{'username': form.username}, {'email': form.email}])
    if response_data.count != 0:
        return create_response(
            message="Username or email already used",
            success=False,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    user_data = form.dict()
    user_data['password'] = encrypt_password(user_data['password'])

    db_user.put(user_data)

    del user_data['password']

    return create_response(
        message="Register successful",
        success=True,
        status_code=status.HTTP_201_CREATED,
        data=user_data
    )


@router.post('/login', tags=['Auth'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    response_data = db_user.fetch([{'username': form_data.username}, {'email': form_data.username}])
    if response_data.count == 0:
        return create_response(
            message="Account information not found",
            success=False,
            status_code=status.HTTP_404_NOT_FOUND
        )

    user_data = response_data.items[0]
    if decrypt_password(user_data['password']) != form_data.password:
        return create_response(
            message="Password wrong",
            success=False,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return_data = {
        'access_token': create_access_token(user_data['username']),
        'refresh_token': create_refresh_token(user_data['username']),
        'token_type': 'bearer'
    }

    return create_response(
        message="Login successful",
        success=True,
        status_code=status.HTTP_200_OK,
        data=return_data
    )










