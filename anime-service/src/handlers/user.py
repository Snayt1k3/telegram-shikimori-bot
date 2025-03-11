import logging

from src.application.dto import Event, ResponseDTO
from src.handlers.ioc import IoC
from src.tasks.sync import start_load_user_rates

logger = logging.getLogger(__name__)


async def user_profile(ioc: IoC, data: Event) -> ResponseDTO:
    try:
        logger.info("Start processing 'user_profile'")

        async with ioc.get_profile() as usecase:
            res = await usecase(data.user_info.id)

        logger.info("Processing complete 'user_profile'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.exception(
            "Error while processing 'user_profile' for user_id={user_id}", exc_info=e
        )
        return {"status": 500, "data": None, "error": str(e)}


async def load_user(ioc: IoC, data: Event) -> ResponseDTO:
    try:
        start_load_user_rates(data.user_info.id)

        return {"status": 200, "data": None, "error": None}
    except Exception as e:
        logger.exception(f"Error occurred while processing 'load_user'", exc_info=e)
        return {"status": 500, "data": None, "error": str(e)}


async def sync_user(ioc: IoC, data: Event) -> ResponseDTO:
    try:
        async with ioc.sync_rates() as usecase:
            usecase(data.user_info.id)

        return {"status": 200, "data": None, "error": None}
    except Exception as e:
        logger.exception(f"Error occurred while processing 'load_user'", exc_info=e)
        return {"status": 500, "data": None, "error": str(e)}
