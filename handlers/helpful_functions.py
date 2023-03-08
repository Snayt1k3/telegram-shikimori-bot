import aiohttp

from bot import db_client
from constants import headers, shiki_url
from .oauth import check_token


async def get_information_from_anime(anime_id: int) -> dict:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"{shiki_url}api/animes/{anime_id}") as response:
            if response.status == 200:
                return await response.json()
            return {}


async def get_user_id(chat_id: int) -> int:
    db_current = db_client['telegram-shiki-bot']
    collection = db_current["ids_users"]
    return collection.find_one({'chat_id': chat_id})['shikimori_id']


def oauth2_decorator(func):
    """Decorator for func"""

    async def wrapper(*args, **kwargs):
        await check_token()
        return await func(*args, **kwargs)

    return wrapper


def oauth2_state(func):
    """Decorator for func with state"""

    async def wrapper(*args, **kwargs):
        await check_token()
        return await func(*args, state=kwargs['state'])

    return wrapper


async def check_anime_already_in_profile(chat_id: int, anime_id: int) -> str:
    id_user = await get_user_id(chat_id)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
                f"{shiki_url}api/v2/user_rates?user_id={id_user}&target_id={anime_id}&target_type=Anime") as response:
            json_file = await response.json()
            if json_file:
                return json_file[0]['status']
            return ''


async def get_animes_by_status_and_id(chat_id: int, status: str) -> list[dict]:
    id_user = await get_user_id(chat_id)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"{shiki_url}"
                               f"api/v2/user_rates?user_id={id_user}&target_type=Anime&status={status}") as response:
            json_dict = await response.json()
            return json_dict


async def get_anime_info_user_rate(chat_id: int, target_id: int) -> list[dict]:
    id_user = await get_user_id(chat_id)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
                f"{shiki_url}api/v2/user_rates?user_id={id_user}&target_type=Anime&target_id={target_id}") as response:
            return await response.json()


async def delete_anime_from_user_profile(target_id: int, chat_id: int) -> int:
    id_user = await get_user_id(chat_id)
    anime_id = await get_anime_info_user_rate(chat_id, target_id)
    anime_id = anime_id[0]['id']
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.delete(f"{shiki_url}api/v2/user_rates/{anime_id}",
                                  json={
                                      "user_rate": {
                                          "user_id": id_user,
                                          "target_type": "Anime"
                                      }
                                  }) as response:
            return response.status


async def add_anime_rate(target_id, chat_id, status, episodes=0) -> int:
    id_user = await get_user_id(chat_id)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(
                f"{shiki_url}api/v2/user_rates", json={
                    "user_rate": {
                        "status": status,
                        "target_id": target_id,
                        "target_type": "Anime",
                        "user_id": id_user,
                        "episodes": episodes
                    }
                }) as response:
            return response.status


async def update_anime_score(target_id, chat_id, score=0):
    id_user = await get_user_id(chat_id)
    info_target = await get_anime_info_user_rate(chat_id, target_id)

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.patch(
                shiki_url + f"api/v2/user_rates/{info_target[0]['id']}",
                json={"user_rate": {
                    "user_id": id_user,
                    "target_type": "Anime",
                    "score": score
                }}) as response:
            return await response.json()


async def update_anime_eps(target_id, chat_id, eps=0):
    id_user = await get_user_id(chat_id)
    info_target = await get_anime_info_user_rate(chat_id, target_id)

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.patch(
                shiki_url + f"api/v2/user_rates/{info_target[0]['id']}",
                json={"user_rate": {
                    "user_id": id_user,
                    "target_type": "Anime",
                    "episodes": eps
                }}) as response:
            return await response.json()
