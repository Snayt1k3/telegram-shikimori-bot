from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Keyboard.inline import cr_kb_by_collection, AnimeMarkEdit_Kb
from bot import dp
from database.database import DataBase
from .helpful_functions import edit_message_for_view_anime, PaginationMarkupLists, \
    AnimeMarkDisplay, AnimeMarkDisplayEdit, DisplayUserLists
from .shikimori_requests import ShikimoriRequests


async def UnlinkUserClk(call: types.CallbackQuery):
    action = call.data.split(".")[0]

    if action == "True":  # delete user from db
        db = DataBase()
        db.trash_collector('chat_id', call.message.chat.id, 'users_id')

        await call.message.answer("☑️ Удалено")
    else:
        await call.message.answer("❌ Отменено")

    await call.message.delete()


async def UserListClk(call: types.CallbackQuery):
    data = call.data.split('.')

    if data[3] == 'next':
        await PaginationMarkupLists(call.message, data[0], "+", int(data[2]))

    elif data[3] == 'prev':
        await PaginationMarkupLists(call.message, data[0], "-", int(data[2]))

    else:
        kb = cr_kb_by_collection(data[0], data[1], data[2])
        user_rate = await ShikimoriRequests.GetAnimeInfoRate(call.message.chat.id, data[1])
        anime_info = await ShikimoriRequests.GetAnimeInfo(data[1])
        await edit_message_for_view_anime(call.message, kb, anime_info, user_rate[0])


async def AnimeEditClk(call: types.CallbackQuery):  # "coll.target_id.page.action.anime_edit"
    datas = call.data.split('.')

    # boring ifs
    if datas[3] == 'delete':
        await ShikimoriRequests.DeleteAnimeProfile(datas[1], call.message.chat.id)
        await call.message.answer('Аниме было удалено из вашего Профиля.')
        await call.message.delete()

    elif datas[3] == 'complete':
        await ShikimoriRequests.AddAnimeRate(datas[1], call.message.chat.id, 'completed')
        await call.message.answer('Аниме было добавлено в ваш список "Просмотрено".')
        await call.message.delete()

    elif datas[3] == 'drop':
        await ShikimoriRequests.AddAnimeRate(datas[1], call.message.chat.id, 'dropped')
        await call.message.answer(f'Аниме было добавлено в ваш список "Брошено".')
        await call.message.delete()

    elif datas[3] == 'watch':
        await ShikimoriRequests.AddAnimeRate(datas[1], call.message.chat.id, 'watching')
        await call.message.answer(f'Аниме было добавлено в ваш список "Смотрю".')
        await call.message.delete()

    elif datas[3] == 'minus':
        info_user_rate = await ShikimoriRequests.GetAnimeInfoRate(call.message.chat.id, datas[1])
        if info_user_rate[0]['episodes'] > 0:
            res = await ShikimoriRequests.UpdateAnimeEps(datas[1], call.message.chat.id,
                                                         info_user_rate[0]['episodes'] - 1)
            await call.message.answer(f'Кол-во просмотренных Эпизодов было обновлено.\n'
                                      f'Просмотренных Эпизодов - {res["episodes"]}')
        else:
            await call.message.answer("Вы еще не посмотрели ни один эпизод.")

    elif datas[3] == 'plus':
        info_user_rate = await ShikimoriRequests.GetAnimeInfoRate(call.message.chat.id, datas[1])
        res = await ShikimoriRequests.UpdateAnimeEps(datas[1], call.message.chat.id,
                                                     info_user_rate[0]['episodes'] + 1)
        await call.message.answer(f'Кол-во просмотренных Эпизодов было обновлено.\n'
                                  f'Просмотренных Эпизодов - {res["episodes"]}')

    elif datas[3] == 'back':
        await DisplayUserLists(call.message, '', datas[0], True, datas[2])

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
        await call.message.answer(f'Оценка Аниме была обновлена.'
                                  f'Текущая оценка - {res["score"]}')


async def AnimeMarkClk(call: types.CallbackQuery):  # "action.id.anime_mark"
    data = call.data.split('.')
    if data[0] == 'cancel':
        await call.message.delete()
        return

    await AnimeMarkDisplayEdit(call.message, data[1])


async def AnimeMarkEditClk(call: types.CallbackQuery):  # 'action.anime_id.anime_mark_edit'
    """callback for view one anime from mark command"""
    data = call.data.split('.')
    info = await ShikimoriRequests.GetAnimeInfoRate(call.message.chat.id, data[1])  # check anime exists in user rates

    if data[0] == 'back':
        await AnimeMarkDisplay(call.message, None, True)

    elif data[0] == 'score':
        if not info:
            await call.message.answer('Данное Аниме не содержится ни в одном вашем списке,\n'
                                      'Вы можете его добавить соответствующими кнопками.')
        else:
            # create kb for change rating
            kb = InlineKeyboardMarkup()
            btns = [InlineKeyboardButton(
                f'{i}',
                callback_data=f'score.{i}.{data[1]}.anime_mark_update_score')
                for i in range(11)
            ]
            kb.row(*btns[:5])
            kb.row(*btns[5:])
            kb.add(InlineKeyboardButton('<<', callback_data=f'back.0.{data[1]}.anime_mark_update_score'))

            await dp.bot.edit_message_reply_markup(
                call.message.chat.id,
                call.message.message_id,
                reply_markup=kb)

    elif data[0] == 'delete':
        if info:
            await ShikimoriRequests.DeleteAnimeProfile(data[1], call.message.chat.id)
        else:
            await call.message.answer('Данное Аниме не содержится ни в одном ваше списке,\n'
                                      'Вы можете его добавить соответствующими кнопками.')
    else:
        await ShikimoriRequests.AddAnimeRate(data[1], call.message.chat.id, data[0])
        await call.message.answer('Аниме было добавлено в выбранный вами список.')


async def AnimeMarkEditUpdateScoreClk(call: types.CallbackQuery):  # 'action.score.anime_id.anime_mark_update_score'
    """callback for anime mark command, editing rating """
    data = call.data.split('.')

    if data[0] == 'back':
        await AnimeMarkDisplayEdit(call.message, data[2])

    else:
        await ShikimoriRequests.UpdateAnimeScore(data[2], call.message.chat.id, data[1])
        await call.message.answer(f'Оценка аниме была обновлена на - {data[1]}')


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(UnlinkUserClk,
                                       lambda call: call.data.split('.')[-1] == 'reset_user')

    dp.register_callback_query_handler(UserListClk,
                                       lambda call: call.data.split('.')[-1] == 'user_list')

    dp.register_callback_query_handler(AnimeEditClk,
                                       lambda call: call.data.split('.')[-1] == 'anime_edit')

    dp.register_callback_query_handler(AnimeMarkClk,
                                       lambda call: call.data.split('.')[-1] == 'anime_mark')

    dp.register_callback_query_handler(AnimeMarkEditClk,
                                       lambda call: call.data.split('.')[-1] == 'anime_mark_edit')

    dp.register_callback_query_handler(UpdateScoreClk,
                                       lambda call: call.data.split('.')[-1] == 'update_score')
    dp.register_callback_query_handler(AnimeMarkEditUpdateScoreClk,
                                       lambda call: call.data.split('.')[-1] == 'anime_mark_update_score')
