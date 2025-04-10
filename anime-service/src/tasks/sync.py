import asyncio
from logging import getLogger

from src.adapters.celery import celery_app
from src.handlers.ioc import IoC
from src.utils import error_handler

logger = getLogger(__name__)


def run_async_task(async_func, *args):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        asyncio.create_task(async_func(*args))
    else:
        asyncio.run(async_func(*args))


@celery_app.task
def start_sync_user_rate(ioc: IoC, rate_id: int) -> None:
    run_async_task(_sync_user_rate, ioc, rate_id)


@celery_app.task
def start_load_user_rates(ioc: IoC, user_id: int) -> None:
    run_async_task(_load_user_rates, ioc, user_id)


@celery_app.task
def start_delete_rate(ioc: IoC, rate_id: int) -> None:
    run_async_task(_delete_user_rate, ioc, rate_id)


@error_handler("delete_user_rate")
async def _delete_user_rate(ioc: IoC, rate_id: int) -> None:
    async with ioc.delete_user_rate_task() as usecase:
        await usecase(rate_id)


@error_handler("sync_user_rate")
async def _sync_user_rate(ioc: IoC, rate_id: int) -> None:
    async with ioc.sync_rate() as usecase:
        await usecase(rate_id)


@error_handler
async def _load_user_rates(ioc: IoC, user_id: int) -> None:
    async with ioc.load_rates() as usecase:
        await usecase(user_id)
