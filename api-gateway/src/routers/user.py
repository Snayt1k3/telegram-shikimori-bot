import uuid

from fastapi import APIRouter
from fastapi.params import Depends

from src.adapters.cache import AbstractCache, RedisCache
from src.adapters.mq_client import message_queue_client
from src.config.kafka import kafka_cfg
from src.dto.auth import User
from src.dto.mq import MQMessage
from src.dto.response import ResponseDTO
from src.utils.hash import convert_to_md5

router = APIRouter(prefix="/user")


@router.post("/profile")
async def get_profile(
    user_info: User, cache: AbstractCache = Depends(RedisCache)
) -> ResponseDTO:
    key = convert_to_md5(f"profile-{user_info.id_telegram}")

    if data := await cache.get(key) is not None:
        return ResponseDTO(error="", status=200, data=data)

    service = message_queue_client()
    response = await service.send_message_and_wait(
        topic=kafka_cfg.ANIME_TOPIC,
        message=MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="get_profile",
            data=None,
            user_info=user_info,
        ),
    )

    await cache.set(key, response, 60 * 5)

    return ResponseDTO(error="", status=200, data=response)


@router.post("/load")
async def load_user_rates(user_info: User) -> ResponseDTO:
    service = message_queue_client()

    response = await service.send_message_and_wait(
        topic=kafka_cfg.ANIME_TOPIC,
        message=MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="load_rates",
            data=None,
            user_info=user_info,
        ),
    )

    return ResponseDTO(error="", status=200, data=response)
