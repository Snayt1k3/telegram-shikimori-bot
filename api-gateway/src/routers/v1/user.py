import uuid

from fastapi import APIRouter

from src.config.kafka import kafka_cfg
from src.dto import ResponseDTO, MQMessage, AuthenticatedUser
from src.routers.dependencies import CacheServiceDep, MessageQueueDep
from src.utils.hash import convert_to_md5

router = APIRouter(prefix="/v1/api/user")


@router.post("/profile")
async def get_profile(
    user: AuthenticatedUser, cache: CacheServiceDep, mq: MessageQueueDep
) -> ResponseDTO:
    key = convert_to_md5(f"profile-{user.telegram_id}")

    if data := await cache.get(key) is not None:
        return ResponseDTO(error="", status=200, data=data)

    response = await mq.send_message_and_wait(
        topic=kafka_cfg.ANIME_TOPIC,
        message=MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="get_profile",
            data=None,
            user_info=user,
        ),
    )

    await cache.set(key, response, 60 * 5)

    return ResponseDTO(error="", status=200, data=response)


@router.post("/load")
async def load_user_rates(user: AuthenticatedUser, mq: MessageQueueDep) -> ResponseDTO:
    # todo: Сделать чтобы не было спаминга на ручка и не перегружался сервис
    response = await mq.send_message_and_wait(
        topic=kafka_cfg.ANIME_TOPIC,
        message=MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="load_rates",
            data=None,
            user_info=user,
        ),
    )

    return ResponseDTO(error="", status=200, data=response)
