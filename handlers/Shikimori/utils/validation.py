from database.database import db_repository
from database.repositories.shikimori import shiki_repository
from handlers.Shikimori.utils.shiki_api import shiki_api


async def check_user_in_database(chat_id) -> bool:
    """
    checking user exists or not in db
    """
    if await db_repository.get_one(filter={"chat_id": chat_id}, collection="users_id"):
        return True
    return False


async def check_user_list(chat_id: int | str, collection: str, status: str) -> None:
    """
    checks the information in the database for relevance

    :param chat_id: telegram id
    :param collection: Mongo collection
    :param status: Type list from shikimori
    """
    animes = await shiki_repository.get_one(collection, {"chat_id": chat_id})
    user_rates = await shiki_api.get_animes_by_status(chat_id, status)

    if set(animes.get("animes")) == set(
        [anime.get("target_id") for anime in user_rates.text]
    ):
        return

    await shiki_repository.update_one(
        collection,
        {"chat_id": chat_id},
        {"animes": [anime.get("target_id") for anime in user_rates.text]},
    )
