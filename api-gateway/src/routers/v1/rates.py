import uuid
from typing import Literal

from fastapi import APIRouter

from src.config.kafka import kafka_cfg
from src.dto import ResponseDTO, RateUpdateDTO, RateAddDTO, MQMessage, AuthenticatedUser
from src.routers.dependencies import CacheServiceDep, MessageQueueDep
from src.utils.filter import filter_none_params
from src.utils.hash import convert_to_md5

router = APIRouter(prefix="/v1/api/rate")


@router.get("/")
async def get_rates(
    status: Literal[
        "completed", "planned", "rewatching", "dropped", "watching", "on_hold"
    ] = None,
    user_id: int = None,
    ids: str = None,
    cache: CacheServiceDep = None,
    mq: MessageQueueDep = None,
):
    key = convert_to_md5(f"{status}-{user_id}-{ids}")

    if data := await cache.get(key) is not None:
        return ResponseDTO(error="", status=200, data=data)

    response = await mq.send_message_and_wait(
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
    data: RateAddDTO, user: AuthenticatedUser, mq: MessageQueueDep
) -> ResponseDTO:
    response = await mq.send_message_and_wait(
        topic=kafka_cfg.ANIME_TOPIC,
        message=MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="add_rate",
            data=data.model_dump(),
            user_info=user,
        ),
    )

    return ResponseDTO(error="", status=200, data=response)


@router.patch("/:rate_id")
async def update_rate(
    rate_id: int, data: RateUpdateDTO, user: AuthenticatedUser, mq: MessageQueueDep
) -> ResponseDTO:
    response = await mq.send_message_and_wait(
        topic=kafka_cfg.ANIME_TOPIC,
        message=MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="update_rate",
            data=data.model_dump() + {"id": rate_id},
            user_info=user,
        ),
    )

    return ResponseDTO(error="", status=200, data=response)


@router.delete("/:rate_id")
async def delete_rate(
    rate_id: int, user: AuthenticatedUser, mq: MessageQueueDep
) -> ResponseDTO:
    response = await mq.send_message_and_wait(
        topic=kafka_cfg.ANIME_TOPIC,
        message=MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="delete_rate",
            data={"id": rate_id},
            user_info=user,
        ),
    )

    return ResponseDTO(error="", status=200, data=response)
