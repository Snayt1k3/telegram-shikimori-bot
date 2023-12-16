from database.database import MongoRepository
from database.schemas.animes import ShikimoriAnime


class ShikimoriRepository(MongoRepository):
    async def insert_shiki_list(
        self, chat_id: int, collection: str, anime_ids: List[int]
    ) -> list[ShikimoriAnime]:
        """
        insert shiki ids in db, but before deleted previous objs
        :param chat_id: telegram chat_id
        :param collection: Mongo Collection
        :param anime_ids: List of anime shiki responses
        """
        try:
            animes_info = await ShikimoriApiClient.get_animes_info(anime_ids)
            animes = [
                ShikimoriAnime(
                    title_ru=anime["russian"],
                    title_en=anime["name"],
                    id=anime["id"],
                )
                for anime in animes_info
            ]

            await super().delete_many(collection, {"chat_id": chat_id})
            await super().create_one(
                collection, {"chat_id": chat_id, "animes": anime_ids}
            )
            return animes
        except Exception as e:
            logging.error(
                f"Error occurred when trying to insert shikilist into db - {e}"
            )

    async def get_shiki_list(
        self, chat_id: int, collection: str
    ) -> list[ShikimoriAnime]:
        """
        :param chat_id: Telegram chat id
        :param collection: name of Mongo collection
        """
        try:
            obj = await super().get_one(collection, {"chat_id": chat_id})

            animes = await ShikimoriApiClient.get_animes_info(obj["animes"])

            return [
                ShikimoriAnime(
                    title_ru=anime["russian"],
                    title_en=anime["name"],
                    id=anime["id"],
                )
                for anime in animes
            ]

        except Exception as e:
            logging.error(
                f"Error occurred when trying to get info about anime form shiki - {e}"
            )
