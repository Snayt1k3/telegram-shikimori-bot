import logging

from src.application.dto import Event
from src.application.dto.response import ResponseDTO
from src.handlers.ioc import IoC

logger = logging.getLogger(__name__)


async def user_profile(ioc: IoC, data: Event) -> ResponseDTO:
    try:
        logger.info("Start processing 'user_profile'")

        # async with ioc.read_title() as usecase:
        #     res = await usecase(**filter_by)

        logger.info("Processing complete 'user_profile'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'user_profile': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}

async def load_user(ioc: IoC, data: Event) -> ResponseDTO:
    try:
        logger.info("Start processing 'user_profile'")

        # async with ioc.read_title() as usecase:
        #     res = await usecase(**filter_by)

        logger.info("Processing complete 'user_profile'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'user_profile': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}




async def start_sync_user(ioc: IoC, user_id: int) -> ResponseDTO:
    try:
        logger.info("Start processing 'user_profile'")

        # async with ioc.read_title() as usecase:
        #     res = await usecase(**filter_by)

        logger.info("Processing complete 'user_profile'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'user_profile': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}
