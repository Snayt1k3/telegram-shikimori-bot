from aiogram import types, Dispatcher

from Keyboard.inline import cr_all_follows_kb, cr_search_kb
from bot import db_client
from .anilibria_handlers import all_follows
from .helpful_functions import get_torrent, get_anime_info_from_al, display_edit_message, display_search_anime, \
    display_anime_which_founds_on_shiki, edit_all_follows_markup
from .notifications import follow_notification, unfollow_notification
from .states import start_shiki_mark_from_al


async def all_follows_callback(call: types.CallbackQuery):
    action = call.data.split('.')[0]
    id_title = call.data.split('.')[1]

    if action == 'prev':
        await edit_all_follows_markup(call.message, '-', page=int(call.data.split('.')[1]))

    elif action == 'next':
        await edit_all_follows_markup(call.message, "+", page=int(call.data.split('.')[1]))

    else:
        anime_info = await get_anime_info_from_al(id_title)
        kb = cr_all_follows_kb(id_title)

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

    elif action == 'shikimori':
        res = await ShikimoriRequests.search_on_shikimori(id_title)
        await display_anime_which_founds_on_shiki(call.message, res)


async def search_anime_al(call: types.CallbackQuery):
    if call.data.split('.')[0] == 'cancel':
        await call.message.delete()
        return

    anime_info = await get_anime_info_from_al(int(call.data.split('.')[0]))
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

    elif action == 'shikimori':
        res = await ShikimoriRequests.search_on_shikimori(id_title)
        await display_anime_which_founds_on_shiki(call.message, res)


async def shikimori_view_founds(call: types.CallbackQuery):
    action = call.data.split('.')[0]

    if action == 'cancel':
        await call.message.delete()
        return

    else:
        db = db_client['telegram-shiki-bot']
        coll = db['shiki_mark_from_al']
        coll.delete_many({'chat_id': call.message.chat.id})
        coll.insert_one({'chat_id': call.message.chat.id,
                         'anime': int(call.data.split('.')[1])})

        eps = await ShikimoriRequests.get_anime_info(call.data.split('.')[1])
        await start_shiki_mark_from_al(call.message, eps['episodes'])


async def get_torrent_callback(call: types.CallbackQuery):
    action = call.data.split('.')[0]

    if action == 'cancel':
        await call.message.delete()
        return

    else:
        await get_torrent(call.message, int(call.data.split('.')[0]))
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

    dp.register_callback_query_handler(shikimori_view_founds,
                                       lambda call: call.data.split('.')[-1] == 'shikimori_founds')

    dp.register_callback_query_handler(get_torrent_callback,
                                       lambda call: call.data.split('.')[-1] == 'get_torrent')
