from fastapi import APIRouter, status

from db import *
from dependencies import create_response


router = APIRouter(prefix='/api/development')


# @router.delete("/database", tags=['Development'])
# async def drop_database():
#     for db in get_all_db():
#         delete_all_items(db)
#
#     return create_response(
#         message="Successfully drop all records",
#         success=True,
#         status_code=status.HTTP_200_OK
#     )
