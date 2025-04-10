import asyncio
import logging

from shikimori import Shikimori

from src.application.dto import JobStatus
from src.application.interfaces import UseCase, AbstractUow

logger = logging.getLogger(__name__)


class ShikimoriLoadAnimes(UseCase):
    def __init__(self, uow: AbstractUow, shiki: Shikimori):
        self._uow = uow
        self._shiki = shiki

    async def __call__(self) -> JobStatus:
        # Загрузка titles с шикимори.
        # А также обновления онгоингов, которые находятся в бд
        # Выгрузка будет ночью когда меньше всего активность
        try:

            fields = """
            {
                id
                malId
                russian
                english
                score
                status
                episodes
                episodesAired
                poster { originalUrl }
            }
            """

            page = 0
            titles = await self._shiki.graphql.animes(fields=fields, page=page, limit=50)
            logger.info("Starting load animes")

            while len(titles) > 50:
                logger.info(f"Loading page - {page}")
                await asyncio.sleep(0.2)

                titles = titles["data"]["animes"]

                for title in titles:
                    title_db = await self._uow.title.find_one(id=title["id"])

                    if not title_db:
                        await self._uow.title.update_one(
                            id=title["id"],
                            mal_id=title["malId"],
                            title_ru=title["russian"],
                            title_en=title["english"],
                            image_url=title["poster"]["originalUrl"],
                            status=title["status"],
                            score=title["score"],
                            episodes=title["episodes"],
                            episodes_aired=title["episodesAired"],
                            volumes=0,
                            chapters=0,
                        )
                    else:
                        await self._uow.title.add_one(
                            id=title["id"],
                            mal_id=title["MalId"],
                            title_ru=title["russian"],
                            title_en=title["english"],
                            image_url=title["poster"]["originalUrl"],
                            status=title["status"],
                            score=title["score"],
                            episodes=title["episodes"],
                            episodes_aired=title["episodesAired"],
                            volumes=0,
                            chapters=0,
                        )

                page += 1
                titles = await self._shiki.graphql.animes(fields=fields, page=page, limit=50)
            logger.info("Ending load animes")
            return JobStatus(error=None, success=True)

        except Exception as e:
            return JobStatus(error=str(e), success=False)


class ShikimoriLoadMangas(UseCase):
    def __init__(self, uow: AbstractUow, shiki: Shikimori):
        self._uow = uow
        self._shiki = shiki

    async def __call__(self) -> JobStatus:
        # Загрузка titles с шикимори.
        # А также обновления онгоингов, которые находятся в бд
        # Выгрузка будет ночью когда меньше всего активность
        try:

            fields = """
            {
                id
                malId
                russian
                english
                score
                status
                volumes
                chapters
                poster { originalUrl }
            }
            """

            page = 0
            titles = await self._shiki.graphql.mangas(fields=fields, page=page, limit=50)
            logger.info("Starting load mangas")

            while len(titles) > 50:
                logger.info(f"Loading page - {page}")
                await asyncio.sleep(0.2)

                titles = titles["data"]["mangas"]

                for title in titles:
                    title_db = await self._uow.title.find_one(id=title["id"])

                    if not title_db:
                        await self._uow.title.update_one(
                            id=title["id"],
                            mal_id=title["malId"],
                            title_ru=title["russian"],
                            title_en=title["english"],
                            image_url=title["poster"]["originalUrl"],
                            status=title["status"],
                            score=title["score"],
                            volumes=title["volumes"],
                            chapters=title["chapters"],
                            episodes=0,
                            episodes_aired=0
                        )
                    else:
                        await self._uow.title.add_one(
                            id=title["id"],
                            mal_id=title["MalId"],
                            title_ru=title["russian"],
                            title_en=title["english"],
                            image_url=title["poster"]["originalUrl"],
                            status=title["status"],
                            score=title["score"],
                            volumes=title["volumes"],
                            chapters=title["chapters"],
                            episodes=0,
                            episodes_aired=0
                        )

                page += 1
                titles = await self._shiki.graphql.mangas(fields=fields, page=page, limit=50)
            logger.info("Ending load mangas")
            return JobStatus(error=None, success=True)

        except Exception as e:
            return JobStatus(error=str(e), success=False)


class MalLoad(UseCase):
    def __init__(self, uow: AbstractUow):
        self._uow = uow

    async def __call__(self) -> JobStatus:
        pass
