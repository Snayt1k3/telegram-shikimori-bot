import logging

from src.domain.entities.base import Entity
from src.handlers.ioc import IoC

logger = logging.getLogger(__name__)


async def read_title(ioc: IoC, filter_by: dict) -> dict:
    try:
        logger.info("Start processing 'read_title'")

        async with ioc.read_title() as usecase:
            res = await usecase(**filter_by)

        logger.info("Processing complete 'read_title'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'read_title': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}
