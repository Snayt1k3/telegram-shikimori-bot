from fastapi import APIRouter
from fastapi.params import Depends

from src.routers.auth.dto import UserAuthDTO, UserCheckDTO
from src.dto import ResponseDTO
from src.adapters.auth import BaseAuth, AuthImpl

router = APIRouter(prefix="/auth")


@router.post("/uri")
async def get_uri(service: BaseAuth = Depends(AuthImpl)) -> ResponseDTO:
    uri = await service.get_uri()
    if uri is None:
        return ResponseDTO(
            error="Something went wrong. Try again", status=500, data=None
        )
    return ResponseDTO(error=None, data={"uri": uri}, status=200)


@router.post("/check")
async def check_user(
    data: UserCheckDTO, service: BaseAuth = Depends(AuthImpl)
) -> ResponseDTO:
    res = await service.check_user(data)
    if res is None:
        return ResponseDTO(error="User not found.", status=404, data=None)
    return ResponseDTO(error=None, status=200, data=res.model_dump())


@router.post("/")
async def auth(data: UserAuthDTO, service: BaseAuth = Depends(AuthImpl)) -> ResponseDTO:
    res = await service.auth_user(data)
    if res is None:
        return ResponseDTO(error="Invalid token.", status=400, data=None)
    return ResponseDTO(error=None, status=200, data=res.model_dump())
