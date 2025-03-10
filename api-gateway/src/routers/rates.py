import uuid
from typing import Literal

from fastapi import APIRouter
from fastapi.params import Depends

from src.adapters.cache import AbstractCache, RedisCache
from src.adapters.mq_client import message_queue_client
from src.config.kafka import kafka_cfg
from src.dto.auth import User
from src.dto.mq import MQMessage
from src.dto.rates import RateUpdateDTO, RateAddDTO
from src.dto.response import ResponseDTO
from src.utils.filter import filter_none_params
from src.utils.hash import convert_to_md5

router = APIRouter(prefix="/rate")


@router.get("/")
async def get_rates(
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ] = None,
    user_id: int = None,
    ids: str = None,
    cache: AbstractCache = Depends(RedisCache),
):
    key = convert_to_md5(f"{status}-{user_id}-{ids}")

    if data := await cache.get(key) is not None:
        return ResponseDTO(error="", status=200, data=data)

    service = message_queue_client()
    response = await service.send_message_and_wait(
        topic=kafka_cfg.ANIME_TOPIC,
        message=MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="read_rates",
            data=filter_none_params(
                {
                    "user_id": user_id,
                    "status": status,
                    "ids": ids.split(",") if ids else None,
                }
            ),
            user_info=None,
        ),
    )

    await cache.set(key, response, 60 * 5)

    return ResponseDTO(error="", status=200, data=response)


@router.post("/")
async def add_rate(
    data: RateAddDTO,
    user_info: User,
) -> ResponseDTO:
    service = message_queue_client()
    response = await service.send_message_and_wait(
        topic=kafka_cfg.ANIME_TOPIC,
        message=MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="add_rate",
            data=data.to_dict(),
            user_info=user_info,
        ),
    )

    return ResponseDTO(error="", status=200, data=response)


@router.patch("/:rate_id")
async def update_rate(
    rate_id: int,
    data: RateUpdateDTO,
    user_info: User,
) -> ResponseDTO:
    service = message_queue_client()
    response = await service.send_message_and_wait(
        topic=kafka_cfg.ANIME_TOPIC,
        message=MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="update_rate",
            data=data.to_dict() + {"id": rate_id},
            user_info=user_info,
        ),
    )

    return ResponseDTO(error="", status=200, data=response)


@router.delete("/:rate_id")
async def delete_rate(
    rate_id: int,
    user_info: User,
) -> ResponseDTO:
    service = message_queue_client()
    response = await service.send_message_and_wait(
        topic=kafka_cfg.ANIME_TOPIC,
        message=MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="delete_rate",
            data={"id": rate_id},
            user_info=user_info,
        ),
    )

    return ResponseDTO(error="", status=200, data=response)
