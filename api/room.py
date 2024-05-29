from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from db import db_room
from dependencies import create_response


router = APIRouter(prefix='/api/room')


@router.get('/')
async def get_all_rooms() -> JSONResponse:
    response_data = db_room.fetch()
    if response_data.count == 0:
        return create_response(
            message="Empty data",
            success=True,
            status_code=status.HTTP_200_OK
        )

    return_data = response_data.items

    return create_response(
        message="Fetch data success",
        success=True,
        status_code=status.HTTP_200_OK,
        data=return_data
    )
