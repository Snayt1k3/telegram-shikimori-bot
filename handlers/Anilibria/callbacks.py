from aiogram import types, Dispatcher

from Keyboard.inline import cr_all_follows_kb, cr_search_kb
from .anilibria_handlers import all_follows, display_search_anime
from .notifications import follow_notification, unfollow_notification
from .helpful_functions import get_torrent, get_anime_info, display_edit_message, display_search_anime


async def all_follows_callback(call: types.CallbackQuery):
    anime_info = await get_anime_info(int(call.data.split('.')[0]))
    kb = cr_all_follows_kb(int(call.data.split('.')[0]))

    await display_edit_message(call.message, kb, anime_info)


async def all_follows_edit_callback(call: types.CallbackQuery):
    action = call.data.split('.')[0]
    id_title = call.data.split('.')[1]

    if action == 'torrent':
        await get_torrent(call.message, int(id_title))

    elif action == 'back':
        await call.message.delete()
        await all_follows(call.message)

    elif action == 'unfollow':
        await unfollow_notification(int(id_title), call.message)
        await call.message.delete()


async def search_anime_al(call: types.CallbackQuery):
    if call.data.split('.')[0] == 'cancel':
        await call.message.delete()
        return

    anime_info = await get_anime_info(int(call.data.split('.')[0]))
    kb = cr_search_kb(call.data.split('.')[0])
    await display_edit_message(call.message, kb, anime_info)


async def search_edit_al(call: types.CallbackQuery):
    action = call.data.split('.')[0]

    id_title = call.data.split('.')[1]

    if action == 'torrent':
        await get_torrent(call.message, int(id_title))

    elif action == 'back':
        await call.message.delete()
        await display_search_anime(call.message)

    elif action == 'follow':
        await follow_notification(int(id_title), call.message)
        await call.message.delete()


def register_al_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(all_follows_edit_callback,
                                       lambda call: call.data.split('.')[-1] == 'all_follows_edit')
    dp.register_callback_query_handler(all_follows_callback,
                                       lambda call: call.data.split('.')[-1] == 'all_follows')

    dp.register_callback_query_handler(search_anime_al,
                                       lambda call: call.data.split('.')[-1] == 'search_al')
    dp.register_callback_query_handler(search_edit_al,
                                       lambda call: call.data.split('.')[-1] == 'search_edit_al')
