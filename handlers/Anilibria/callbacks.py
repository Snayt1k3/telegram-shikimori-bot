from aiogram import types, Dispatcher

from Keyboard.inline import cr_all_follows_kb, cr_search_kb
from bot import anilibria_client
from database.database import DataBase
from handlers.Shikimori.shikimori_requests import ShikimoriRequests
from .handlers import all_follows
from .helpful_functions import get_torrent, display_edit_message, display_search_anime, \
    display_anime_which_founds_on_shiki, edit_all_follows_markup
from .notifications import follow_notification, unfollow_notification
from .states import start_shiki_mark_from_al


async def AllFollowsClk(call: types.CallbackQuery):  # "action.target_id/page.all_follows"
    data = call.data.split('.')

    if data[0] == 'prev':
        await edit_all_follows_markup(call.message, '-', page=int(data[1]))

    elif data[0] == 'next':
        await edit_all_follows_markup(call.message, "+", page=int(data[1]))

    else:
        anime_info = await anilibria_client.get_title(int(data[1]))
        kb = cr_all_follows_kb(data[1])

        await display_edit_message(call.message, kb, anime_info)


async def AllFollowsEditClk(call: types.CallbackQuery):
    data = call.data.split('.')

    if data[0] == 'torrent':
        await get_torrent(call.message, int(data[1]))

    elif data[0] == 'back':
        await call.message.delete()
        await all_follows(call.message)

    elif data[0] == 'unfollow':
        await unfollow_notification(int(data[1]), call)

    elif data[0] == 'shikimori':
        res = await ShikimoriRequests.SearchShikimori(data[1])
        await display_anime_which_founds_on_shiki(call.message, res)


async def SearchAnimeClk(call: types.CallbackQuery):
    if call.data.split('.')[0] == 'cancel':
        await call.message.delete()
        return

    anime_info = await anilibria_client.get_title(int(call.data.split('.')[0]))
    kb = cr_search_kb(call.data.split('.')[0])
    await display_edit_message(call.message, kb, anime_info)


async def SearchEditClk(call: types.CallbackQuery):
    data = call.data.split('.')

    if data[0] == 'torrent':
        await get_torrent(call.message, int(data[1]))

    elif data[0] == 'back':
        await call.message.delete()
        await display_search_anime(call.message)

    elif data[0] == 'follow':
        await follow_notification(int(data[1]), call)

    elif data[0] == 'shikimori':
        res = await ShikimoriRequests.SearchShikimori(data[1])
        await display_anime_which_founds_on_shiki(call.message, res)


async def ShikimoriFoundsClk(call: types.CallbackQuery):
    action = call.data.split('.')[0]

    if action == 'cancel':
        await call.message.delete()
        return

    else:
        await DataBase.trash_collector('chat_id', call.message.chat.id, 'shiki_mark_from_al')
        await DataBase.insert_into_collection('shiki_mark_from_al', {'chat_id': call.message.chat.id,
                                                                     'anime': int(call.data.split('.')[1])})
        eps = await ShikimoriRequests.GetAnimeInfo(call.data.split('.')[1])
        await start_shiki_mark_from_al(call.message, eps['episodes'])


async def GetTorrentClk(call: types.CallbackQuery):
    action = call.data.split('.')[0]

    if action == 'cancel':
        await call.message.delete()
        return

    else:
        await get_torrent(call.message, int(call.data.split('.')[0]))


def register_al_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(AllFollowsEditClk,
                                       lambda call: call.data.split('.')[-1] == 'all_follows_edit')
    dp.register_callback_query_handler(AllFollowsClk,
                                       lambda call: call.data.split('.')[-1] == 'all_follows')

    dp.register_callback_query_handler(SearchAnimeClk,
                                       lambda call: call.data.split('.')[-1] == 'search_al')
    dp.register_callback_query_handler(SearchEditClk,
                                       lambda call: call.data.split('.')[-1] == 'search_edit_al')

    dp.register_callback_query_handler(ShikimoriFoundsClk,
                                       lambda call: call.data.split('.')[-1] == 'shikimori_founds')

    dp.register_callback_query_handler(GetTorrentClk,
                                       lambda call: call.data.split('.')[-1] == 'get_torrent')
