from fastapi import APIRouter

from src.dto.auth import AuthData, CheckData
from src.dto.response import ResponseDTO

router = APIRouter(prefix="auth")


@router.post("/")
async def auth_user(data: AuthData) -> ResponseDTO: ...


@router.get("/uri")
async def get_uri() -> ResponseDTO: ...


@router.post("/check")
async def check_user(data: CheckData) -> ResponseDTO: ...
