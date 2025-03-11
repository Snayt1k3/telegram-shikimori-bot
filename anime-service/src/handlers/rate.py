import logging

from src.application.dto import Event
from src.application.dto.response import ResponseDTO
from src.handlers.ioc import IoC

logger = logging.getLogger(__name__)


async def read_rates(ioc: IoC, data: Event) -> ResponseDTO:
    try:
        logger.info("Start processing 'read_rates'")

        async with ioc.read_rates() as usecase:
            res = await usecase(data.data)

        logger.info("Processing completed 'read_rates'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'read_rates': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def delete_rate(ioc: IoC, data: Event) -> ResponseDTO:
    try:
        logger.info("Start processing 'delete_rate'")

        async with ioc.delete_rate() as usecase:
            res = await usecase(data.data)

        logger.info("Processing completed 'delete_rate'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'delete_rate': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def update_rate(ioc: IoC, data: Event) -> ResponseDTO:
    try:
        logger.info("Start processing 'update_rate'")

        async with ioc.update_rate() as usecase:
            res = await usecase(data.data)

        logger.info("Processing completed 'update_rate'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'update_rate': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def add_rate(ioc: IoC, data: Event) -> ResponseDTO:
    try:
        logger.info("Start processing 'add_rate'")

        async with ioc.add_rate() as usecase:
            res = await usecase(data.data)

        logger.info("Processing completed 'add_rate'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'add_rate': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}
