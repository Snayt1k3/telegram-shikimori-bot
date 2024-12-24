from fastapi import APIRouter

from src.dto.rate import RateUpdateDTO, RateFilterDTO
from src.dto.response import ResponseDTO

router = APIRouter(prefix="/rate")


@router.post("/many")
async def get_rates(data: RateFilterDTO):
    pass


@router.patch("/")
async def update_rate(data: RateUpdateDTO) -> ResponseDTO:
    pass


@router.delete("/")
async def delete_rate(id: int) -> ResponseDTO:
    pass
