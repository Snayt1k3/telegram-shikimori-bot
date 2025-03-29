import asyncio
from logging import getLogger

from src.adapters.celery import celery_app
from src.adapters.storage.models.base import get_session
from src.application.dto.job import JobStatus
from src.handlers.ioc import IoC

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
def start_sync_user_rate(rate_id: int) -> None:
    run_async_task(_sync_user_rate, rate_id)


@celery_app.task
def start_load_user_rates(user_id: int) -> None:
    run_async_task(_load_user_rates, user_id)

@celery_app.task
def start_delete_rate(rate_id: int) -> None:
    run_async_task(_delete_user_rate, rate_id)

async def _delete_user_rate(rate_id: int) -> None:
    ioc = IoC(get_session())

    try:
        logger.info(f"Start deleting user rate, id={rate_id}")

        async with ioc.delete_user_rate_task() as usecase:
            result: JobStatus = await usecase(rate_id)

            if result.success:
                logger.info(f"deleting user rate, id={rate_id} done successfully")
            else:
                logger.error(
                    f"Error when deleting rate, id={rate_id}, error={result.error}"
                )

    except Exception as e:
        logger.exception(f"Unexpected error when deleting rate, id={rate_id}: {e}")

async def _sync_user_rate(rate_id: int) -> None:
    ioc = IoC(get_session())

    try:
        logger.info(f"Start syncing user rate, id={rate_id}")

        async with ioc.sync_rate() as usecase:
            result: JobStatus = await usecase(rate_id)

            if result.success:
                logger.info(f"Syncing user rate, id={rate_id} done successfully")
            else:
                logger.error(
                    f"Error when syncing rate, id={rate_id}, error={result.error}"
                )

    except Exception as e:
        logger.exception(f"Unexpected error when syncing rate, id={rate_id}: {e}")


async def _load_user_rates(user_id: int) -> None:
    ioc = IoC(get_session())

    try:
        logger.info(f"Start loading user rates, user_id={user_id}")

        async with ioc.load_rates() as usecase:
            result: JobStatus = await usecase(user_id)

            if result.success:
                logger.info(f"Loading user rates, user_id={user_id} done successfully")
            else:
                logger.error(
                    f"Error when loading rates, user_id={user_id}, error={result.error}"
                )

    except Exception as e:
        logger.exception(f"Unexpected error when loading rates, user_id={user_id}: {e}")
