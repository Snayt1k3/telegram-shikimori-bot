from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from src.dto.auth import UserAuthDTO, UserCheckDTO
from src.dto import ResponseDTO
from src.adapters.auth import BaseAuth, AuthImpl

router = APIRouter(prefix="/auth")


@router.post("/uri")
async def get_uri(service: BaseAuth = Depends(AuthImpl)) -> ResponseDTO:
    uri = await service.get_uri()
    if uri is None:
        raise HTTPException(detail="Something went wrong. Try again", status_code=500)
    return ResponseDTO(error=None, data={"uri": uri}, status=200)


@router.post("/check")
async def check_user(
    data: UserCheckDTO, service: BaseAuth = Depends(AuthImpl)
) -> ResponseDTO:
    res = await service.check_user(data)
    if res is None:
        raise HTTPException(detail="User not found.", status_code=404)
    return ResponseDTO(error=None, status=200, data=res.model_dump())


@router.post("/")
async def auth(data: UserAuthDTO, service: BaseAuth = Depends(AuthImpl)) -> ResponseDTO:
    res = await service.auth_user(data)
    if res is None:
        raise HTTPException(
            detail="Invalid token.",
            status_code=400,
        )
    return ResponseDTO(error=None, status=200, data=res.model_dump())
