from fastapi import APIRouter
from fastapi.params import Depends

from src.dto.auth import UserAuthDTO, UserCheckDTO
from src.dto.response import ResponseDTO
from src.adapters.auth import BaseAuth, AuthImpl

router = APIRouter(prefix="/auth")


@router.post("/uri")
async def get_uri(service: BaseAuth = Depends(AuthImpl)) -> ResponseDTO:
    uri = await service.get_uri()
    return ResponseDTO(error=None, data={"uri": uri}, status=200)


@router.post("/check")
async def check_user(
    data: UserCheckDTO, service: BaseAuth = Depends(AuthImpl)
) -> ResponseDTO:
    res = await service.check_user(data)
    return ResponseDTO(error=None, status=200, data=res.model_dump())


@router.post("/")
async def auth(data: UserAuthDTO, service: BaseAuth = Depends(AuthImpl)) -> ResponseDTO:
    res = await service.auth_user(data)
    return ResponseDTO(error=None, status=200, data=res.model_dump())
