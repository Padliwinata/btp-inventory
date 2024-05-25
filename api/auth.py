from fastapi import status
from fastapi.responses import JSONResponse

from base import router
from db import *
from dependencies import create_response, encrypt_password
from schemas.auth import RegisterForm


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
async def login()

