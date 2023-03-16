import aiohttp
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hlink

from bot import db_client, dp
from handlers.Anilibria.helpful_functions import get_anime_info_from_al
from handlers.translator import translate_text
from misc.constants import get_headers, shiki_url
from .oauth import check_token


async def get_info_anime_from_shiki(target_id) -> dict:
    async with aiohttp.ClientSession(headers=get_headers()) as session:
        async with session.get(f"{shiki_url}api/animes/{target_id}") as response:
            if response.status == 200:
                return await response.json()
            return {}


async def get_shiki_id_by_chat_id(chat_id: int):
    db_current = db_client['telegram-shiki-bot']
    collection = db_current["ids_users"]
    try:
        return collection.find_one({'chat_id': chat_id})['shikimori_id']
    except TypeError:
        return None


def oauth2(func):
    """Decorator Func, implements check oauth"""

    async def wrapper(*args, **kwargs):
        await check_token()
        return await func(*args, **kwargs)

    return wrapper


@oauth2
async def check_anime_already_in_profile(chat_id: int, target_id: int) -> str:
    """This function not required, but just for beautiful display, if anime already in user profile"""
    id_user = await get_shiki_id_by_chat_id(chat_id)
    async with aiohttp.ClientSession(headers=get_headers()) as session:
        async with session.get(
                f"{shiki_url}api/v2/user_rates?user_id={id_user}&target_id={target_id}&target_type=Anime") as response:
            json_file = await response.json()
            if json_file:
                return json_file[0]['status']
            return ''


@oauth2
async def get_animes_by_status_and_id(chat_id: int, status: str) -> list[dict]:
    id_user = await get_shiki_id_by_chat_id(chat_id)
    async with aiohttp.ClientSession(headers=get_headers()) as session:
        async with session.get(f"{shiki_url}"
                               f"api/v2/user_rates?user_id={id_user}&target_type=Anime&status={status}") as response:
            json_dict = await response.json()
            return json_dict


@oauth2
async def get_anime_info_user_rate(chat_id: int, target_id) -> list[dict]:
    """this method make a get request
    :return list with one dict"""
    id_user = await get_shiki_id_by_chat_id(chat_id)
    async with aiohttp.ClientSession(headers=get_headers()) as session:
        async with session.get(
                f"{shiki_url}api/v2/user_rates?user_id={id_user}&target_type=Anime&target_id={target_id}") as response:
            return await response.json()


@oauth2
async def delete_anime_from_user_profile(target_id: int, chat_id: int) -> int:
    """This function delete an anime from user profile on shikimori
    :return response.status_code"""
    id_user = await get_shiki_id_by_chat_id(chat_id)
    anime_id = await get_anime_info_user_rate(chat_id, target_id)
    anime_id = anime_id[0]['id']
    async with aiohttp.ClientSession(headers=get_headers()) as session:
        async with session.delete(f"{shiki_url}api/v2/user_rates/{anime_id}",
                                  json={
                                      "user_rate": {
                                          "user_id": id_user,
                                          "target_type": "Anime"
                                      }
                                  }) as response:
            return response.status


@oauth2
async def add_anime_rate(target_id, chat_id, status, episodes=0) -> int:
    """This function add an anime into profile user on shikimori
    :return response.status_code"""
    id_user = await get_shiki_id_by_chat_id(chat_id)
    async with aiohttp.ClientSession(headers=get_headers()) as session:
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


@oauth2
async def update_anime_score(target_id, chat_id, score=0):
    """This function make a patch request, if we have score, score can be score"""
    id_user = await get_shiki_id_by_chat_id(chat_id)
    info_target = await get_anime_info_user_rate(chat_id, target_id)

    async with aiohttp.ClientSession(headers=get_headers()) as session:
        async with session.patch(
                shiki_url + f"api/v2/user_rates/{info_target[0]['id']}",
                json={"user_rate": {
                    "user_id": id_user,
                    "target_type": "Anime",
                    "score": score
                }}) as response:
            return await response.json()


@oauth2
async def update_anime_eps(target_id, chat_id, eps=0):
    """This function make a patch request, if we have eps, eps can be updated"""
    id_user = await get_shiki_id_by_chat_id(chat_id)
    info_target = await get_anime_info_user_rate(chat_id, target_id)

    async with aiohttp.ClientSession(headers=get_headers()) as session:
        async with session.patch(
                shiki_url + f"api/v2/user_rates/{info_target[0]['id']}",
                json={"user_rate": {
                    "user_id": id_user,
                    "target_type": "Anime",
                    "episodes": eps
                }}) as response:
            return await response.json()


@oauth2
async def search_on_shikimori(id_title) -> list[dict]:
    """
    :param id_title: this id from anilibria.tv not from shikimori
    :return: list of animes which founds
    """
    anime_info = await get_anime_info_from_al(id_title)

    # request to shikimori
    async with aiohttp.ClientSession(headers=get_headers()) as session:
        async with session.get(shiki_url + f"api/animes?search={anime_info['names']['en']}&limit=7") as response:
            return await response.json()


async def edit_message_for_view_anime(message: types.Message, kb, anime_info, user_rate):
    await dp.bot.edit_message_media(types.InputMediaPhoto(shiki_url + anime_info['image']['original']), message.chat.id,
                                    message.message_id)

    await dp.bot.edit_message_caption(message.chat.id, message.message_id,
                                      reply_markup=kb,
                                      parse_mode='HTML',
                                      caption=f"<b>Eng</b>: {anime_info['name']}  \n"
                                              f"<b>Rus</b>: {anime_info['russian']} \n"
                                              f"<b>Rating</b>: {anime_info['score']}\n"
                                              f"<b>Your Rating</b>: {user_rate['score']}\n"
                                              f"<b>Viewed</b>: {user_rate['episodes']} "
                                              f": {anime_info['episodes']} \n" +
                                              hlink(await translate_text(message, 'Go to the Anime'),
                                                    shiki_url + anime_info['url'])
                                      )


async def edit_reply_markup_user_lists(message: types.Message, coll, action, page):
    """This func implements pagination for planned, watching, completed lists, by Keyboard,
    this method edit Keyboard(Inline) for Each page"""

    # Get DB, collection
    db_current = db_client['telegram-shiki-bot']
    collection = db_current[coll]

    # get user list
    record = collection.find_one({'chat_id': message.chat.id})

    # action with page
    if action == '-':
        page -= 8
    else:
        page += 8

    kb = InlineKeyboardMarkup()

    for anime in record['animes'][page: page + 8]:
        anime_info = await get_info_anime_from_shiki(anime)
        kb.add(InlineKeyboardButton(anime_info['russian'],
                                    callback_data=f"{coll}.{anime}.{page}.view.user_list"))

    # Kb actions
    if len(record['animes']) > page + 8 and page != 0:
        kb.add(
            InlineKeyboardButton(text='<<Prev', callback_data=f'{coll}.0.{page}.prev.user_list'),
            InlineKeyboardButton(text='Next>>', callback_data=f'{coll}.0.{page}.next.user_list'),
        )

    elif page != 0:
        kb.add(
            InlineKeyboardButton(text='<<Prev', callback_data=f'{coll}.0.{page}.prev.user_list'))
    else:
        kb.add(
            InlineKeyboardButton(text='Next>>', callback_data=f'{coll}.0.{page}.next.user_list'),
        )

    await dp.bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=kb)


async def start_pagination_user_lists(message: types.Message, status, coll, list_name):
    # get required datas
    animes = await get_animes_by_status_and_id(message.chat.id, status)

    # get DB
    db_current = db_client['telegram-shiki-bot']
    collection = db_current[coll]

    # trash collector
    collection.delete_many({'chat_id': chat_id})

    # write into db
    collection.insert_one({'chat_id': message.chat.id,
                           "animes": [anime['target_id'] for anime in animes]})

    # Keyboard object
    kb = InlineKeyboardMarkup()

    for anime in animes[:8]:
        # get anime name
        anime_info = await get_info_anime_from_shiki(anime['target_id'])

        # add pretty buttons for action with user list
        kb.add(InlineKeyboardButton(text=anime_info['russian'],
                                    callback_data=f"{coll}.{anime['target_id']}.0.view.user_list"))
    # check list for pagination
    if len(animes) > 8:
        kb.add(InlineKeyboardButton('Next >>',
                                    callback_data=f"{coll}.0.0.next.user_list"))

    await dp.bot.send_photo(message.chat.id, open('misc/follows.png', 'rb'),
                            reply_markup=kb,
                            caption=await translate_text(message, 'Выберите Интересующее вас аниме, '
                                                                  f'из вашего списка {list_name}'))
