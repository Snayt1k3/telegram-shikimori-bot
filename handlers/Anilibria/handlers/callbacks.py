from aiogram import types, Dispatcher

from Keyboard.inline import all_follows_main_kb
from bot import anilibria_client
from handlers.Anilibria.handlers.handlers import all_follows
from handlers.Anilibria.keyboards import inline
from handlers.Anilibria.utils.message import (
    get_torrent,
    display_edit_message,
    anime_from_shikimori_msg,
    edit_all_follows_markup,
    shiki_mark_message,
    search_anime_msg,
)
from handlers.Anilibria.utils.notifications import (
    follow_notification,
    unfollow_notification,
)
from handlers.Shikimori.shikimori_requests import ShikimoriRequests


async def all_follows_callback(call: types.CallbackQuery, callback_data: dict):
    anime_id = callback_data.get("anime_id")
    anime_info = await anilibria_client.get_title(int(anime_id))
    kb = await all_follows_main_kb(anime_id)
    await display_edit_message(call.message, kb, anime_info)


async def all_follows_actions_callback(call: types.CallbackQuery):
    data = call.data.split(".")

    match data[0]:
        case "torrent":
            await get_torrent(call.message, int(data[1]))
        case "back":
            await call.message.delete()
            await all_follows(call.message)
        case "unfollow":
            await unfollow_notification(int(data[1]), call)
        case "shikimori":
            res = await ShikimoriRequests.SearchShikimori(data[1])
            await anime_from_shikimori_msg(call.message, res)


async def search_anime_callback(call: types.CallbackQuery, callback_data: dict):
    anime_id = int(callback_data.get("anime_id"))
    anime_info = await anilibria_client.get_title(anime_id)
    kb = await inline.search_actions_keyboard(anime_info.id)
    await display_edit_message(call.message, kb, anime_info)


async def search_actions_callback(call: types.CallbackQuery):
    data = call.data.split(".")

    match data[0]:
        case "torrent":
            await get_torrent(call.message, int(data[1]))
        case "back":
            await call.message.delete()
            await search_anime_msg(call.message)
        case "follow":
            await follow_notification(int(data[1]), call)
        case "shikimori":
            res = await ShikimoriRequests.SearchShikimori(data[1])
            await anime_from_shikimori_msg(call.message, res)


async def shikimori_mark_callback(call: types.CallbackQuery, callback_data: dict):
    await shiki_mark_message(call.message, callback_data.get("anime_id"))


async def get_torrent_callback(call: types.CallbackQuery):
    action = call.data.split(".")[0]

    if action == "cancel":
        await call.message.delete()
        return

    else:
        await get_torrent(call.message, int(call.data.split(".")[0]))


async def cancel(call: types.CallbackQuery):
    await call.message.delete()


def register_al_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(cancel, inline.cancel_clk.filter())

    dp.register_callback_query_handler(
        all_follows_actions_callback,
        lambda call: call.data.split(".")[-1] == "all_follows_edit",
    )
    dp.register_callback_query_handler(
        all_follows_callback, inline.all_follows_clk.filter()
    )

    dp.register_callback_query_handler(
        search_anime_callback, inline.search_anilibria_clk.filter()
    )
    dp.register_callback_query_handler(
        search_actions_callback,
        lambda call: call.data.split(".")[-1] == "search_edit_al",
    )

    dp.register_callback_query_handler(
        shikimori_mark_callback, inline.search_shikimori_clk.filter()
    )

    dp.register_callback_query_handler(
        get_torrent_callback, lambda call: call.data.split(".")[-1] == "get_torrent"
    )
