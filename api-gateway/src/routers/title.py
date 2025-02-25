import uuid

from fastapi import APIRouter

from src.adapters.mq_client import message_queue_client
from src.dto.mq import MQMessage
from src.dto.response import ResponseDTO
from src.settings.kafka import kafka_settings
from src.utils.filter import filter_none_params

router = APIRouter(prefix="/title")


@router.get("/")
async def get_titles(
    title_ru: str = None,
    title_en: str = None,
    score: str = None,
    status: str = None,
    ids: str = None,
) -> ResponseDTO:
    service = message_queue_client()
    response = await service.send_message_and_wait(
        topic=kafka_settings.ANIME_TOPIC,
        message=MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="read_titles",
            data=filter_none_params(
                {
                    "title_ru": title_ru,
                    "ids": ids.split(",") if ids else None,
                    "status": status,
                    "title_en": title_en,
                    "score": score,
                }
            ),
            user_info=None,
        ),
    )

    return ResponseDTO(error="", status=200, data=response)
