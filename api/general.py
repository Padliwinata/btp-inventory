from fastapi import APIRouter, status

from db import db_roles
from dependencies import create_response

router = APIRouter(prefix='/api/general')


# @router.get('/role')
# async def get_roles():
#     response_data = db_role.fetch()
#     if response_data.count == 0:
#         return create_response(
#             message="Empty data",
#             success=True,
#             status_code=status.HTTP_200_OK
#         )
#
#     return create_response(
#         message="Success fetch data",
#         success=True,
#         status_code=status.HTTP_200_OK,
#         data={'roles': response_data.items}
#     )


