from fastapi import APIRouter

from src.dto.response import ResponseDTO
from src.dto.title import TitleFilterDTO

router = APIRouter(prefix="/title")


@router.post("/many")
async def get_titles(data: TitleFilterDTO) -> ResponseDTO:
    pass
