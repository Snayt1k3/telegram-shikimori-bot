from logging import getLogger

from src.adapters.celery import celery_app
from src.handlers.ioc import IoC
from src.tasks.sync import run_async_task

logger = getLogger(__name__)


@celery_app.task
def start_load_titles(*args) -> None:
    run_async_task(load_titles, *args)


async def load_titles(ioc: IoC) -> None:
    async with ioc.shikimori_load_animes() as usecase:
        res = await usecase

    logger.info(f"Result of loading anime: success - {res.success}; error - {res.error}")

    async with ioc.shikimori_load_mangas() as usecase:
        res = await usecase

    logger.info(f"Result of loading anime: success - {res.success}; error - {res.error}")
