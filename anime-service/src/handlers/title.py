import logging

from src.application.dto.response import ResponseDTO
from src.handlers.ioc import IoC

logger = logging.getLogger(__name__)


async def read_title(ioc: IoC, filter_by: dict) -> ResponseDTO:
    try:
        logger.info("Start processing 'read_title'")

        async with ioc.read_title() as usecase:
            res = await usecase(**filter_by)

        logger.info("Processing complete 'read_title'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'read_title': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def read_many_titles(ioc: IoC, filter_by: dict) -> ResponseDTO:
    try:
        logger.info("Start processing 'read_titles'")

        async with ioc.read_titles() as usecase:
            res = await usecase(**filter_by)

        logger.info("Processing complete 'read_titles'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'read_titles': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def add_title(ioc: IoC, obj: dict) -> ResponseDTO:
    try:
        logger.info("Start processing 'add_title'")

        async with ioc.add_title() as usecase:
            res = await usecase(**obj)

        logger.info("Processing complete 'add_title'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'add_title': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def add_titles(ioc: IoC, objs: list[dict]) -> ResponseDTO:
    try:
        logger.info("Start processing 'add_titles'")

        async with ioc.add_titles() as usecase:
            res = await usecase(objs)

        logger.info("Processing complete 'add_titles'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'add_titles': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def update_titles(ioc: IoC, objs: list[dict]) -> ResponseDTO:
    try:
        logger.info("Start processing 'update_titles'")

        async with ioc.update_titles() as usecase:
            res = await usecase(objs)

        logger.info("Processing complete 'update_titles'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'update_titles': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def update_title(ioc: IoC, obj: dict) -> ResponseDTO:
    try:
        logger.info("Start processing 'update_title'")

        async with ioc.update_title() as usecase:
            res = await usecase(**obj)

        logger.info("Processing complete 'update_title'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'update_title': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def delete_title(ioc: IoC, id: int) -> ResponseDTO:
    try:
        logger.info("Start processing 'delete_title'")

        async with ioc.delete_title() as usecase:
            res = await usecase(id=id)

        logger.info("Processing complete 'delete_title'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'delete_title': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}


async def delete_titles(ioc: IoC, id: int) -> ResponseDTO:
    try:
        logger.info("Start processing 'delete_titles'")

        async with ioc.delete_title() as usecase:
            res = await usecase(id=id)

        logger.info("Processing complete 'delete_titles'")

        return {"status": 200, "data": res, "error": None}
    except Exception as e:
        logger.error(f"Error occurred while processing 'delete_titles': {str(e)}")
        return {"status": 500, "data": None, "error": str(e)}
