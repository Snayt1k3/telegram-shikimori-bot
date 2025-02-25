import uuid

from fastapi import APIRouter, Depends

from src.adapters.request import RequestInterface
from src.dto import MQMessage
from src.dto.response import ResponseDTO
from src.dto.title import TitleFilterDTO

router = APIRouter(prefix="/title")


@router.get("/")
async def get_titles(
    data: TitleFilterDTO, service: RequestInterface = Depends()
) -> ResponseDTO:
    response = await service.send_message_and_wait(
        MQMessage(
            correlation_id=uuid.uuid4(),
            event_type="read_titles",
            data=data.to_dict(),
            user_info=None,
        )
    )

    return ResponseDTO(error="", status=200, data=response)
