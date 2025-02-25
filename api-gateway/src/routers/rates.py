import uuid

from fastapi import APIRouter
from fastapi.params import Depends

from src.adapters.mq_client import MessageQueueClientI, message_queue_client
from src.dto.mq import MQMessage
from src.dto.rates import RateUpdateDTO, RateFilterDTO, RateAddDTO
from src.dto.auth import User
from src.dto.response import ResponseDTO

router = APIRouter(prefix="/rate")


@router.get("/")
async def get_rates(
    data: RateFilterDTO,
    user_info: User,
    service: MessageQueueClientI = Depends(message_queue_client),
):
    response = await service.send_message_and_wait(
        MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="read_rates",
            data=data.to_dict(),
            user_info=user_info,
        )
    )

    return ResponseDTO(error="", status=200, data=response)


@router.post("/")
async def add_rate(
    data: RateAddDTO,
    user_info: User,
    service: MessageQueueClientI = Depends(message_queue_client),
) -> ResponseDTO:
    response = await service.send_message_and_wait(
        MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="add_rate",
            data=data.to_dict(),
            user_info=user_info,
        )
    )

    return ResponseDTO(error="", status=200, data=response)


@router.patch("/:rate_id")
async def update_rate(
    rate_id: int,
    data: RateUpdateDTO,
    user_info: User,
    service: MessageQueueClientI = Depends(message_queue_client),
) -> ResponseDTO:
    response = await service.send_message_and_wait(
        MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="update_rate",
            data=data.to_dict() + {"id": rate_id},
            user_info=user_info,
        )
    )

    return ResponseDTO(error="", status=200, data=response)


@router.delete("/:rate_id")
async def delete_rate(
    rate_id: int,
    user_info: User,
    service: MessageQueueClientI = Depends(message_queue_client),
) -> ResponseDTO:
    response = await service.send_message_and_wait(
        MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="delete_rate",
            data={"id": rate_id},
            user_info=user_info,
        )
    )

    return ResponseDTO(error="", status=200, data=response)
