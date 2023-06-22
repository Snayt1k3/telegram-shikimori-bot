from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Keyboard.inline import cr_kb_by_collection
from bot import dp
from database.database import DataBase
from handlers.translator import translate_text
from .helpful_functions import edit_message_for_view_anime, edit_reply_markup_user_lists, anime_search_edit, \
    display_user_list, anime_search_edit_back
from .shikimori_requests import ShikimoriRequests


async def UnlinkUserClk(call: types.CallbackQuery):
    action = call.data.split(".")[0]

    if action == "True":  # delete user from db
        db = DataBase()
        db.trash_collector('chat_id', call.message.chat.id, 'ids_users')

        await call.message.answer(await translate_text(call.message, "☑️ Deleted"))
    else:
        await call.message.answer(await translate_text(call.message, "❌ Cancelled"))

    await call.message.delete()


async def UserListClk(call: types.CallbackQuery):
    data = call.data.split('.')

    if data[3] == 'next':
        await edit_reply_markup_user_lists(call.message, data[0], "+", int(data[2]))

    elif data[3] == 'prev':
        await edit_reply_markup_user_lists(call.message, data[0], "-", int(data[2]))

    else:
        kb = cr_kb_by_collection(data[0], data[1], data[2])
        user_rate = await ShikimoriRequests.GetAnimeInfoRate(call.message.chat.id, data[1])
        anime_info = await ShikimoriRequests.GetAnimeInfo(data[1])
        await edit_message_for_view_anime(call.message, kb, anime_info, user_rate[0])


async def AnimeSearchClk(call: types.CallbackQuery):  # action.target_id.anime_search
    data = call.data.split('.')

    if data[0] == 'view':
        await anime_search_edit(call.message, data[1])

    else:
        await call.message.delete()


async def AnimeEditClk(call: types.CallbackQuery):  # "coll.target_id.page.action.anime_edit"
    datas = call.data.split('.')

    # boring ifs
    if datas[3] == 'delete':
        await ShikimoriRequests.DeleteAnimeProfile(datas[1], call.message.chat.id)
        await call.message.answer(await translate_text(call.message, f'Anime was deleted from your profile'))
        await call.message.delete()
    elif datas[3] == 'complete':
        await ShikimoriRequests.AddAnimeRate(datas[1], call.message.chat.id, 'completed')
        await call.message.answer(await translate_text(call.message, f'Anime was added to completed list'))
        await call.message.delete()

    elif datas[3] == 'drop':
        await ShikimoriRequests.AddAnimeRate(datas[1], call.message.chat.id, 'dropped')
        await call.message.answer(await translate_text(call.message, f'Anime was added to dropped list'))
        await call.message.delete()

    elif datas[3] == 'watch':
        await ShikimoriRequests.AddAnimeRate(datas[1], call.message.chat.id, 'watching')
        await call.message.answer(await translate_text(call.message, f'Anime was added to watching list'))
        await call.message.delete()

    elif datas[3] == 'minus':
        info_user_rate = await ShikimoriRequests.GetAnimeInfoRate(call.message.chat.id, datas[1])
        if info_user_rate[0]['episodes'] > 0:
            res = await ShikimoriRequests.UpdateAnimeEps(datas[1], call.message.chat.id,
                                                         info_user_rate[0]['episodes'] - 1)
            await call.message.answer(await translate_text(call.message, f'Anime episodes has been updated, '
                                                                         f'viewed episodes - {res["episodes"]}'))
        else:
            await call.message.answer(await translate_text(call.message, "You haven't watched a single episode yet"))

    elif datas[3] == 'plus':
        info_user_rate = await ShikimoriRequests.GetAnimeInfoRate(call.message.chat.id, datas[1])
        res = await ShikimoriRequests.UpdateAnimeEps(datas[1], call.message.chat.id,
                                                     info_user_rate[0]['episodes'] + 1)
        await call.message.answer(await translate_text(call.message, f'Anime episodes has been updated, '
                                                                     f'current episodes - {res["episodes"]}'))

    elif datas[3] == 'back':
        await display_user_list(call.message, datas[0], datas[2])

    else:
        kb = InlineKeyboardMarkup(row_width=5)
        btns = [InlineKeyboardButton(text=f'{i}', callback_data=f"{i}.{datas[1]}.{datas[1]}.{datas[2]}.update_score")
                for i in range(0, 11)]

        kb.row(*btns[:5])
        kb.row(*btns[5:])

        kb.add(InlineKeyboardButton('<<', callback_data=f"back.{datas[1]}.{datas[0]}.{datas[2]}.update_score"))
        await dp.bot.edit_message_caption(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                          reply_markup=kb,
                                          caption="📃 Select Rating")


async def UpdateScoreClk(call: types.CallbackQuery):  # "action/score.target_id.coll.page.update_score"
    datas = call.data.split('.')

    if datas[0] == 'back':
        anime_info = await ShikimoriRequests.GetAnimeInfo(datas[1])
        user_rate = await ShikimoriRequests.GetAnimeInfoRate(call.message.chat.id, datas[1])
        kb = cr_kb_by_collection(datas[2], datas[1], datas[3])
        await edit_message_for_view_anime(call.message, kb, anime_info, user_rate[0])

    else:
        res = await ShikimoriRequests.UpdateAnimeScore(call.data.split('.')[1], call.message.chat.id, int(datas[0]))
        await call.message.answer(await translate_text(call.message, f'Anime score has been updated, '
                                                                     f'current score - {res["score"]}'))


async def AnimeSearchEditClk(call: types.CallbackQuery):   # action.target_id.anime_search_edit
    data = call.data.split('.')

    if data[0] == 'completed' or data[0] == 'planned':
        await ShikimoriRequests.AddAnimeRate(data[1], call.message.chat.id, data[0])
        await call.message.answer(await translate_text(call.message,
                                                       f"Anime has been added to your {data[0]} list"))
        await call.message.delete()

    else:
        await anime_search_edit_back(call.message)


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(UnlinkUserClk, lambda call: call.data.split('.')[-1] == 'reset_user')
    dp.register_callback_query_handler(AnimeSearchClk, lambda call: call.data.split('.')[-1] == 'anime_search')
    dp.register_callback_query_handler(AnimeSearchEditClk,
                                       lambda call: call.data.split('.')[-1] == 'anime_search_edit')

    dp.register_callback_query_handler(UserListClk, lambda call: call.data.split('.')[-1] == 'user_list')
    dp.register_callback_query_handler(AnimeEditClk, lambda call: call.data.split('.')[-1] == 'anime_edit')

    dp.register_callback_query_handler(UpdateScoreClk, lambda call: call.data.split('.')[-1] == 'update_score')
