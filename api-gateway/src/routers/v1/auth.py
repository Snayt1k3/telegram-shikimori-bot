from fastapi import APIRouter, HTTPException

from src.dto import ResponseDTO, UserGetRequest, UserAuthRequest
from src.routers.dependencies import AuthServiceDep

router = APIRouter(prefix="/v1/api/auth")


@router.get("/uri")
async def get_uri(service: AuthServiceDep) -> ResponseDTO:
    uri = await service.get_uri()
    if uri is None:
        raise HTTPException(detail="Something went wrong. Try again", status_code=500)
    return ResponseDTO(error=None, data={"uri": uri}, status=200)


@router.post("/user")
async def get_user(data: UserGetRequest, service: AuthServiceDep) -> ResponseDTO:
    res = await service.get_user(data)
    return ResponseDTO(error=None, status=200, data=res.model_dump())


@router.post("/")
async def auth(data: UserAuthRequest, service: AuthServiceDep) -> ResponseDTO:
    res = await service.auth_user(data)
    if res is None:
        raise HTTPException(detail="Invalid token.", status_code=400)

    return ResponseDTO(error=None, status=200, data=res.model_dump())
