import logging

from src.application.dto import Event, ResponseDTO
from src.handlers.ioc import IoC
from src.utils import error_handler

logger = logging.getLogger(__name__)


@error_handler("read_rates")
async def read_rates(ioc: IoC, data: Event) -> ResponseDTO:
    async with ioc.read_rates() as usecase:
        res = await usecase(data.data)

    return {"status": 200, "data": res, "error": None}


@error_handler("delete_rate")
async def delete_rate(ioc: IoC, data: Event) -> ResponseDTO:
    async with ioc.delete_rate() as usecase:
        res = await usecase(data.data)

    return {"status": 200, "data": res, "error": None}


@error_handler("update_rate")
async def update_rate(ioc: IoC, data: Event) -> ResponseDTO:
    async with ioc.update_rate() as usecase:
        res = await usecase(data.data)

    return {"status": 200, "data": res, "error": None}


@error_handler("add_rate")
async def add_rate(ioc: IoC, data: Event) -> ResponseDTO:
    async with ioc.add_rate() as usecase:
        res = await usecase(data.data)

    return {"status": 200, "data": res, "error": None}
