import asyncio

from shikimori import Shikimori

from src.application.interfaces import AbstractUow, UseCase


class LoadAllUserRates(UseCase):
    """
    Loading all user rates from user profile on shikimori.
    """

    def __init__(self, uow: AbstractUow, shiki: Shikimori) -> None:
        self.shiki = shiki
        self.uow = uow

    async def __call__(self, user_id: int) -> None:
        user_rates = []
        page = 1
        while True:
            rates = await self.shiki.graphql.userRates(
                """
                {
                id
                chapters 
                episodes
                rewatches
                score
                status
                volumes
                anime {
                  id
                  name
                  russian
                  episodes
                  episodesAired
                  malId
                  poster {
                    originalUrl
                  }
                  score
                  status
                }
                manga {
                  id
                  name
                  russian
                  volumes
                  chapters
                  malId
                  poster {
                    originalUrl
                  }
                  score
                  status
                }
              }
            }
            """,
                page=page,
                limit=50,
            )
            await asyncio.sleep(0.2)
            user_rates.extend(rates)

            if rates != 50:
                break

            page += 1

        async with self.uow as uow:
            all_user_rates = await uow.user_rate.find_many(user_id=user_id)
            rates_ids = set(i.id for i in all_user_rates)

            for rate in user_rates:
                if rate["id"] in rates_ids:
                    continue

                title_id = rate.get("anime", {}).get("id", None)

                if not title_id:
                    title_id = rate.get("manga", {}).get("id")

                title_db = await uow.title.find_one(id=title_id)

                if not title_db:
                    title = rate.get("anime") or rate.get("manga")
                    title_db = await uow.title.add_one(
                        id=title["id"],
                        mal_id=title["malId"],
                        title_ru=title["russian"],
                        title_en=title["name"],
                        image_url=title["poster"]["originalUrl"],
                        status=title["status"],
                        score=title["score"],
                        episodes=title.get("episodes"),
                        episodes_aired=title.get("episodes_aired"),
                        volumes=title.get("volumes"),
                        chapters=title.get("chapters"),
                    )

                await uow.user_rate.add_one(
                    id=rate["id"],
                    user_id=user_id,
                    title_id=title_db.id,
                    target_type="Anime" if rate.get("Anime") else "Manga",
                    score=rate["score"],
                    status=rate["status"],
                    episodes=rate["episodes"],
                    chapters=rate["chapters"],
                    volumes=rate["volumes"],
                    rewatches=rate["rewatches"],
                )
