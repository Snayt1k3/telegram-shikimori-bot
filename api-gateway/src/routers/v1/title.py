import uuid
from typing import Literal

from fastapi import APIRouter, Query

from src.config import kafka_cfg
from src.dto import MQMessage, ResponseDTO
from src.routers.dependencies import CacheServiceDep, MessageQueueDep
from src.utils import filter_none_params, convert_to_md5

router = APIRouter(prefix="/v1/api/title")


@router.get("/")
async def get_titles(
    title_ru: str = Query(
        default=None, description="Anime title in Russian (partial match supported)"
    ),
    title_en: str = Query(
        default=None, description="Anime title in English (partial match supported)"
    ),
    score: int = Query(
        default=None, description="Minimum Shikimori anime score (e.g., '7')", le=10
    ),
    status: Literal["anons", "ongoing", "released"] = Query(
        default=None,
        description="Anime release status: 'anons', 'ongoing', or 'released'",
    ),
    ids: str = Query(
        default=None, description="Comma-separated list of anime IDs (e.g., '1,2,3')"
    ),
    cache: CacheServiceDep = None,
    mq: MessageQueueDep = None,
) -> ResponseDTO:
    key = convert_to_md5(f"{title_ru}-{title_en}-{score}-{status}-{ids}")

    if data := await cache.get(key) is not None:
        return ResponseDTO(error="", status=200, data=data)

    response = await mq.send_message_and_wait(
        topic=kafka_cfg.ANIME_TOPIC,
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

    await cache.set(key, response, 60 * 5)

    return ResponseDTO(error="", status=200, data=response)
