import logging

from src.application.dto.response import ResponseDTO
from src.handlers.ioc import IoC

logger = logging.getLogger(__name__)


async def read_rate(ioc: IoC, **filter_by: dict) -> ResponseDTO:
    try:
        logger.info("Start processing 'read_rate'")

        async with ioc.read_rate() as usecase:
            res = await usecase(**filter_by)

        logger.info("Processing complete 'read_rate'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'read_rate': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def read_rates(ioc: IoC, **filter_by: dict) -> ResponseDTO:
    try:
        logger.info("Start processing 'read_rates'")

        async with ioc.read_rates() as usecase:
            res = await usecase(**filter_by)

        logger.info("Processing complete 'read_rates'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'read_rates': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def delete_rates(ioc: IoC, **filter_by: dict) -> ResponseDTO:
    try:
        logger.info("Start processing 'delete_rates'")

        async with ioc.delete_rates() as usecase:
            res = await usecase(**filter_by)

        logger.info("Processing complete 'delete_rates'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'delete_rates': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def delete_rate(ioc: IoC, **filter_by: dict) -> ResponseDTO:
    try:
        logger.info("Start processing 'delete_rate'")

        async with ioc.delete_rate() as usecase:
            res = await usecase(**filter_by)

        logger.info("Processing complete 'delete_rate'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'delete_rate': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def update_rate(ioc: IoC, **filter_by: dict) -> ResponseDTO:
    try:
        logger.info("Start processing 'update_rate'")

        async with ioc.update_rate() as usecase:
            res = await usecase(**filter_by)

        logger.info("Processing complete 'update_rate'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'update_rate': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def update_rates(ioc: IoC, **filter_by: dict) -> ResponseDTO:
    try:
        logger.info("Start processing 'update_rates'")

        async with ioc.update_rates() as usecase:
            res = await usecase(**filter_by)

        logger.info("Processing complete 'update_rates'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'update_rates': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def add_rates(ioc: IoC, **filter_by: dict) -> ResponseDTO:
    try:
        logger.info("Start processing 'add_rates'")

        async with ioc.add_rates() as usecase:
            res = await usecase(**filter_by)

        logger.info("Processing complete 'add_rates'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'add_rates': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def add_rate(ioc: IoC, **filter_by: dict) -> ResponseDTO:
    try:
        logger.info("Start processing 'add_rate'")

        async with ioc.add_rate() as usecase:
            res = await usecase(**filter_by)

        logger.info("Processing complete 'add_rate'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'add_rate': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}
