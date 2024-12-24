from fastapi import APIRouter

from src.dto.response import ResponseDTO

router = APIRouter(prefix="/auth")


@router.post("/uri")
async def get_uri() -> ResponseDTO: ...


@router.post("/check")
async def check_user() -> ResponseDTO: ...


@router.post("/")
async def auth() -> ResponseDTO: ...
