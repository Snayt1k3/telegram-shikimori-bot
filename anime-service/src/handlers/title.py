import logging

from src.application.dto import Event, ResponseDTO
from src.handlers.ioc import IoC
from src.utils import error_handler
from src.tasks.load import start_load_titles

logger = logging.getLogger(__name__)


@error_handler("read_titles")
async def read_titles(ioc: IoC, data: Event) -> ResponseDTO:
    async with ioc.read_titles() as usecase:
        res = await usecase(data.data)

    return {"status": 200, "data": res, "error": None}


@error_handler("shikimori_load_titles")
async def load_titles(ioc: IoC, data: Event) -> ResponseDTO:
    start_load_titles(ioc)
    return {"status": 200, "data": None, "error": None}

