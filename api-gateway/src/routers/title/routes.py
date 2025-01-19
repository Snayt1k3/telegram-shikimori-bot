import uuid

from fastapi import APIRouter, Depends

from src.adapters.request import RequestInterface
from src.dto import MQMessage
from src.dto.response import ResponseDTO
from src.routers.title.dto import TitleFilterDTO

router = APIRouter(prefix="/title")


@router.get("/many")
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

    if response is not None:
        return ResponseDTO(error="", status=200, data=response)

    return ResponseDTO(
        error="Error occurred, while getting titles", status=400, data=None
    )
