import logging

from src.application.dto import Event
from src.application.dto.response import ResponseDTO
from src.handlers.ioc import IoC

logger = logging.getLogger(__name__)


async def read_titles(ioc: IoC, data: Event) -> ResponseDTO:
    try:
        logger.info("Start processing 'read_titles'")

        async with ioc.read_titles() as usecase:
            res = await usecase(data.data)

        logger.info("Processing complete 'read_titles'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'read_titles': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}
