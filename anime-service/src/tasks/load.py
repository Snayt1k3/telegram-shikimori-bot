from logging import getLogger

from shikimori import RequestError

from src.adapters.celery import celery_app
from src.adapters.storage.models.base import get_session

from src.tasks.sync import run_async_task
from src.utils import retry

logger = getLogger(__name__)


@celery_app.task
def start_load_titles() -> None:
    from src.handlers.ioc import IoC
    run_async_task(load_titles, IoC(get_session()))


@retry((RequestError,))
async def load_titles(ioc) -> None:
    async with ioc.shikimori_load_animes() as usecase:
        res = await usecase

    logger.info(
        f"Result of loading anime: success - {res.success}; error - {res.error}"
    )

    async with ioc.shikimori_load_mangas() as usecase:
        res = await usecase

    logger.info(
        f"Result of loading anime: success - {res.success}; error - {res.error}"
    )
