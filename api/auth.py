from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from db import *
from dependencies import create_response, encrypt_password, decrypt_password, create_refresh_token, create_access_token, get_user
from models import UserDB
from schemas.auth import RegisterForm, CustomResponseDev

router = APIRouter(prefix='/api')


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

    # user_role = db_role.get(user_data['role'])
    # if not user_role:
    #     return create_response(
    #         message="Invalid role key",
    #         success=False,
    #         status_code=status.HTTP_400_BAD_REQUEST
    #     )

    role_data = db_role.fetch({'name': 'staff'})

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

    access_token = create_access_token(user_data['username'])
    refresh_token = create_refresh_token(user_data['username'])

    return_data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }

    resp_dev = CustomResponseDev(
        success=True,
        code=status.HTTP_200_OK,
        message="Authenticated",
        data=return_data,
        access_token=access_token
    )
    return JSONResponse(
        resp_dev.dict(),
        status_code=status.HTTP_200_OK
    )

    # return create_response(
    #     message="Login successful",
    #     success=True,
    #     status_code=status.HTTP_200_OK,
    #     data=return_data
    # )


@router.get('/check', tags=['Auth'])
async def check_authorization(user: UserDB = Depends(get_user)):
    return create_response(
        message="Authorized",
        success=True,
        status_code=status.HTTP_200_OK,
        data=user.dict()
    )







