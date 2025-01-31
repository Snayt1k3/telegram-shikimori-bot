import uuid

from fastapi import APIRouter
from fastapi.params import Depends, Body

from src.adapters.request import RequestInterface
from src.routers.auth import User
from src.dto.mq import MQMessage
from src.routers.rate.dto import RateUpdateDTO, RateFilterDTO, RateAddDTO
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

    return ResponseDTO(
        error="Error occurred, while getting rates", status=400, data=None
    )


@router.patch("/")
async def update_rate(
    data: RateUpdateDTO, user_info: User, service: RequestInterface = Depends()
) -> ResponseDTO:
    response = await service.send_message_and_wait(
        MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="update_rate",
            data=data.to_dict(),
            user_info=user_info,
        )
    )

    if response is not None:
        return ResponseDTO(error="", status=200, data=response)

    return ResponseDTO(
        error="Error occurred, while updating rate", status=400, data=None
    )


@router.post("/")
async def add_rate(
    data: RateAddDTO, user_info: User, service: RequestInterface = Depends()
) -> ResponseDTO:
    response = await service.send_message_and_wait(
        MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="add_rate",
            data=data.to_dict(),
            user_info=user_info,
        )
    )

    if response is not None:
        return ResponseDTO(error="", status=200, data=response)

    return ResponseDTO(error="Error occurred, while adding rate", status=400, data=None)


@router.delete("/")
async def delete_rate(
    id: int, user_info: User, service: RequestInterface = Depends()
) -> ResponseDTO:
    response = await service.send_message_and_wait(
        MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="add_rate",
            data={"id": id},
            user_info=user_info,
        )
    )

    if response is not None:
        return ResponseDTO(error="", status=200, data=response)

    return ResponseDTO(
        error="Error occurred, while deleting rate", status=400, data=None
    )
