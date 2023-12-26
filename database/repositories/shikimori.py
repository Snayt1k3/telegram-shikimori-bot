import logging

from database.database import MongoRepository
from database.dto.animes import ShikimoriAnime


class ShikimoriRepository(MongoRepository):
    async def insert_shiki_list(
        self, chat_id: int, collection: str, animes: list[dict]
    ) -> list[ShikimoriAnime] | None:
        """
        insert shiki ids in db, but before deleted previous objs
        :param chat_id: telegram chat_id
        :param collection: Mongo Collection
        :param animes: List of animes
        """
        try:
            animes = [
                ShikimoriAnime(
                    title_ru=anime["russian"],
                    title_en=anime["name"],
                    id=anime["id"],
                )
                for anime in animes
            ]

            await super().delete_many(collection, {"chat_id": chat_id})
            await super().create_one(
                collection,
                {"chat_id": chat_id, "animes": [anime.__dict__ for anime in animes]},
            )
            return animes
        except Exception as e:
            logging.error(
                f"Error occurred when trying to insert shikilist into db - {e}"
            )

    async def get_shiki_list(
        self, chat_id: int, collection: str
    ) -> list[ShikimoriAnime] | None:
        """
        :param chat_id: Telegram chat id
        :param collection: name of Mongo collection
        """
        try:
            obj = await super().get_one(collection, {"chat_id": chat_id})

            if not obj:
                return None

            return [
                ShikimoriAnime(
                    title_ru=anime["russian"],
                    title_en=anime["name"],
                    id=anime["id"],
                )
                for anime in obj["animes"]
            ]

        except Exception as e:
            logging.error(f"Error occurred when trying to get info from db - {e}")

    async def update_tokens(self, chat_id: int | str, data: dict):
        try:
            return await super().update_one(
                "users_id",
                {
                    "chat_id": chat_id,
                },
                {
                    "access_token": data["access_token"],
                    "refresh_token": data["refresh_token"],
                },
            )

        except Exception as e:
            logging.error(f"Error occurred while update tokens - {e}")

    async def get_shikimori_id(self, chat_id: int | str) -> int:
        try:
            return (
                await super().get_one(
                    "users_id",
                    {
                        "chat_id": chat_id,
                    },
                )
            ).get("shikimori_id")

        except Exception as e:
            logging.error(f"Error occurred while get id - {e}")


shiki_repository = ShikimoriRepository()
