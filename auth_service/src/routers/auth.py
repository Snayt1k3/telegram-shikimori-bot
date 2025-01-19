from fastapi import APIRouter
from fastapi.params import Depends

from src.routers.auth.dto import AuthData, CheckData
from src.dto.response import ResponseDTO
from src.ioc import IoC

router = APIRouter(prefix="auth")


@router.post("/")
async def auth_user(data: AuthData, ioc: Depends(IoC)) -> ResponseDTO:
    async with ioc.auth_user() as usecase:
        return await usecase(data)


@router.get("/uri")
async def get_uri(ioc: Depends(IoC)) -> ResponseDTO:
    async with ioc.get_uri() as usecase:
        return await usecase()


@router.post("/check")
async def check_user(data: CheckData, ioc: Depends(IoC)) -> ResponseDTO:
    async with ioc.check_user() as usecase:
        return await usecase(data)
