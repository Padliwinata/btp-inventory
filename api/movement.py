from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dependencies import get_user
from models import UserDB
from schemas.movement import MovementRequest

router = APIRouter(prefix='/api/movement')

# @router.post('/request')
# async def request_goods_movement(request: MovementRequest, user: UserDB = Depends(get_user)) -> JSONResponse:
#

