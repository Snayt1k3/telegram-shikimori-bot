import uuid

from fastapi import APIRouter
from fastapi.params import Depends

from src.adapters.request import RequestInterface
from src.dto import User
from src.dto.mq import MQMessage
from src.dto.rate import RateUpdateDTO, RateFilterDTO
from src.dto.response import ResponseDTO

router = APIRouter(prefix="/rate")


@router.get("/many")
async def get_rates(
    data: RateFilterDTO, user_info: User, service: RequestInterface = Depends()
):
    response = await service.send_message_and_wait(
        MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="read_rates",
            data=data.to_dict(),
            user_info=user_info,
        )
    )

    if response is not None:
        return ResponseDTO(error="", status=200, data=response)

    return ResponseDTO(error="Something went wrong.", status=400, data=None)


@router.patch("/")
async def update_rate(
    data: RateUpdateDTO, user_info: User, service: RequestInterface = Depends()
) -> ResponseDTO:
    pass


@router.post("/")
async def add_rate(
    anime_id: int, user_info: User, service: RequestInterface = Depends()
) -> ResponseDTO:
    return


@router.delete("/")
async def delete_rate(
    id: int,
    user_info: User,
) -> ResponseDTO:
    pass
