from fastapi import APIRouter

from src.dto.response import ResponseDTO
from src.dto.title import TitleFilterDTO

router = APIRouter(prefix="/title")


@router.get("/many")
async def get_titles(data: TitleFilterDTO) -> ResponseDTO:
    pass
