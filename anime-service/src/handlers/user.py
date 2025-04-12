import logging

from src.application.dto import Event, ResponseDTO
from src.handlers.ioc import IoC
from src.tasks.sync import start_load_user_rates
from src.utils import error_handler

logger = logging.getLogger(__name__)


@error_handler("get_user_profile")
async def user_profile(ioc: IoC, data: Event) -> ResponseDTO:
    async with ioc.get_profile() as usecase:
        res = await usecase(data.user_info.id)

    return {"status": 200, "data": res, "error": None}


@error_handler("loading_user_rates")
async def load_user(ioc: IoC, data: Event) -> ResponseDTO:
    start_load_user_rates(data.user_info.id)
    return {"status": 200, "data": None, "error": None}
