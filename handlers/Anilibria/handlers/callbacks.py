from aiogram import types, Dispatcher

from bot import anilibria_client
from database.repositories.anilibria import anilibria_repository
from handlers.Anilibria.keyboards import inline
from handlers.Anilibria.utils.message import (
    get_torrent,
    edit_message_by_title,
    anime_from_shikimori_msg,
    shiki_mark_message,
)
from handlers.Anilibria.utils.notifications import (
    follow_notification,
    unfollow_notification,
)
from handlers.Shikimori.shikimori_requests import ShikimoriRequests


async def all_follows_callback(call: types.CallbackQuery, callback_data: dict):
    anime_id = callback_data.get("anime_id")
    page = int(callback_data.get("page"))
    anime_info = await anilibria_client.get_title(int(anime_id))
    kb = await inline.all_follows_edit_kb(anime_id, page)
    await edit_message_by_title(call.message, kb, anime_info)


async def all_follows_pagination_clk(call: types.CallbackQuery, callback_data: dict):
    """pagination with user follows list"""
    action = callback_data.get("action")
    page = int(callback_data.get("page"))
    follows = await anilibria_repository.get_all_follows_by_user(call.message.chat.id)

    if action == "prev":
        kb = await inline.all_follows_kb(follows.follows, page=page - 8)
    else:
        kb = await inline.all_follows_kb(follows.follows, page=page + 8)

    await call.message.edit_reply_markup(kb)


async def all_follows_back_clk(call: types.CallbackQuery, callback_data: dict):
    """callback for 'back' button in user follows list when is editing anime"""
    page = int(callback_data.get("page"))
    follows = await anilibria_repository.get_all_follows_by_user(call.message.chat.id)
    kb = await inline.all_follows_kb(follows.follows, page)

    await call.message.edit_media(
        types.InputMediaPhoto(open("misc/img/pic2.png", "rb"))
    )
    await call.message.edit_caption(
        "Нажмите на интересующее вас аниме",
        reply_markup=kb,
    )


async def search_anime_callback(call: types.CallbackQuery, callback_data: dict):
    anime_id = int(callback_data.get("anime_id"))
    anime_info = await anilibria_client.get_title(anime_id)
    kb = await inline.search_actions_keyboard(anime_info.id)
    await edit_message_by_title(call.message, kb, anime_info)


async def search_anime_back_clk(call: types.CallbackQuery, callback_data: dict) -> None:
    """callback for 'back' button when user searching anime on anilibria.tv"""
    animes = await anilibria_repository.get_anilibria_list(
        call.message.chat.id, "anilibria_search"
    )
    kb = await inline.search_anime_kb(animes[:10])

    await call.message.edit_media(
        types.InputMediaPhoto(open("misc/img/pic2.png", "rb"))
    )
    await call.message.edit_caption(
        "Нажмите на интересующее вас аниме", reply_markup=kb
    )


async def shikimori_mark_callback(call: types.CallbackQuery, callback_data: dict):
    await shiki_mark_message(call.message, callback_data.get("anime_id"))


async def get_torrent_callback(call: types.CallbackQuery, callback_data: dict):
    """start process for getting torrent"""
    await get_torrent(call.message, int(callback_data.get("anime_id")))


async def cancel(call: types.CallbackQuery) -> None:
    """deleting message"""
    await call.message.delete()


async def anime_follow(call: types.CallbackQuery, callback_data: dict) -> None:
    """start anime follow process"""
    await follow_notification(int(callback_data.get("anime_id")), call)


async def anime_unfollow(call: types.CallbackQuery, callback_data: dict) -> None:
    """start anime unfollow process"""
    await unfollow_notification(int(callback_data.get("anime_id")), call)


async def search_on_shikimori(call: types.CallbackQuery, callback_data: dict) -> None:
    res = await ShikimoriRequests.SearchShikimori(callback_data.get("anime_id"))
    await anilibria_repository.create_one(
        "shikimori_results_from_anilibria",
        {
            "chat_id": call.message.chat.id,
            "animes": [
                {
                    "name": anime["name"],
                    "russian": anime["russian"],
                    "id": anime["id"],
                }
                for anime in res
            ],
        },
    )
    await anime_from_shikimori_msg(call.message, res)


async def shikimori_back_clk(call: types.CallbackQuery):
    titles = await anilibria_repository.get_one(
        "shikimori_results_from_anilibria", {"chat_id": call.message.chat.id}
    )
    kb = await inline.animes_from_shikimori_kb(titles["animes"])
    await call.message.edit_media(
        types.InputMediaPhoto(open("misc/img/pic2.png", "rb"))
    )
    await call.message.edit_caption(
        caption="Нажмите на интересующее вас аниме",
        reply_markup=kb,
    )


def register_al_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(
        anime_follow, inline.anime_follow_clk.filter(action="follow")
    )
    dp.register_callback_query_handler(
        anime_unfollow, inline.anime_follow_clk.filter(action="unfollow")
    )
    dp.register_callback_query_handler(cancel, inline.cancel_clk.filter())

    dp.register_callback_query_handler(
        all_follows_callback, inline.all_follows_clk.filter()
    )
    dp.register_callback_query_handler(
        all_follows_pagination_clk, inline.all_follows_pagination.filter()
    )
    dp.register_callback_query_handler(
        all_follows_back_clk, inline.all_follows_back.filter()
    )

    dp.register_callback_query_handler(
        search_anime_callback, inline.search_anilibria_clk.filter()
    )
    dp.register_callback_query_handler(
        search_anime_back_clk, inline.search_anilibria_back_clk.filter()
    )

    dp.register_callback_query_handler(
        shikimori_mark_callback, inline.search_shikimori_clk.filter()
    )

    dp.register_callback_query_handler(
        shikimori_back_clk, inline.search_shikimori_back_clk.filter()
    )

    dp.register_callback_query_handler(
        get_torrent_callback, inline.torrent_clk.filter()
    )

    dp.register_callback_query_handler(
        search_on_shikimori, inline.search_shikimori_start_clk.filter()
    )
