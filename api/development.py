from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from base import router
from db import *
from dependencies import create_response, encrypt_password, decrypt_password, create_refresh_token, create_access_token


@router.delete("/database", tags=['Development'])
async def drop_database():
    for db in get_all_db():
        delete_all_items(db)

    return create_response(
        message="Successfully drop all records",
        success=True,
        status_code=status.HTTP_200_OK
    )
