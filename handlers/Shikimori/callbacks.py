from aiogram import Dispatcher, types

from bot import db_client
from handlers.translator import translate_text
from .helpful_functions import get_information_from_anime, get_user_id, delete_anime_from_user_profile, \
    add_anime_rate, update_anime_eps, get_anime_info_user_rate
from .shikimori_profile import display_anime_on_message
from .states import UpdateScore, UpdateScoreCompleted
from handlers.Anilibria.notifications import follow_notification

async def reset_user_callback(call: types.CallbackQuery):
    # get choose user
    data = call.data.split(".")[1]

    if data == "True":
        # Db connect
        db_current = db_client['telegram-shiki-bot']
        # get collection
        collection = db_current["ids_users"]
        collection.delete_one({'chat_id': call.message.chat.id})
        await call.message.answer(await translate_text(call.message, "Deleted"))
    else:
        await call.message.answer(await translate_text(call.message, "❌ Cancelled"))

    await call.message.delete()


async def callback_watch_anime_edit(call: types.CallbackQuery):
    """This callback realize anime from watch_list edit"""
    # DB actions
    db_current = db_client['telegram-shiki-bot']

    # Change collection, for actions on anime
    collection = db_current['anime_watching']

    # Find user watching_list
    id_user = await get_user_id(call.message.chat.id)
    watch_list = collection.find_one({"id_user": id_user})

    action = call.data.split(".")[1]

    if action == 'back':
        await display_anime_on_message(call.message, 'anime_watching')

    if action == 'delete':
        # Here make a request(DELETE), delete from watch_list
        status = await delete_anime_from_user_profile(watch_list['animes'][watch_list['page']]['target_id'],
                                                      call.message.chat.id)
        if status == 204:
            await call.message.answer(f"✔️ {await translate_text(call.message, 'Anime was deleted')}")
        else:
            await call.message.answer(f"❌️ {await translate_text(call.message, 'Anime not deleted')}")

    if action == 'minus' or action == 'add':
        # get anime data and curr episode
        ep = await get_anime_info_user_rate(call.message.chat.id, watch_list['animes'][watch_list['page']]['target_id'])
        ep = ep[0]['episodes']

        # make actions with episode
        if action == 'minus':
            ep -= 1

        elif action == 'add':
            ep += 1

        # make a patch request, for update count episode
        res = await update_anime_eps(watch_list['animes'][watch_list['page']]['target_id'], call.message.chat.id, ep)

        if res:
            await display_anime_on_message(call.message, 'anime_watching', is_edit=True)
            await call.message.answer(f"✔️ {await translate_text(call.message, 'Anime was Updated, current eps')} - "
                                      f"{res['episodes']}")

        else:
            await call.message.answer(f"❌ {await translate_text(call.message, 'Something went wrong')}")

    if action == 'complete':
        # get data and status
        anime_info = await get_information_from_anime(watch_list['animes'][watch_list['page']]['target_id'])
        status = await add_anime_rate(watch_list['animes'][watch_list['page']]['target_id'], call.message.chat.id,
                                      'completed', episodes=anime_info['episodes'])

        if status == 201:
            await call.message.answer(f"✔️ {await translate_text(call.message, 'Anime was Updated')}")
            await call.message.delete()
            return

        else:
            await call.message.answer(f"❌ {await translate_text(call.message, 'Something went wrong')}")

    if action == 'update_score':
        await call.message.answer(await translate_text(call.message, "Write an anime score 1-10"))
        await UpdateScore.score.set()

    await call.message.delete()


async def callback_anime_planned_edit(call: types.CallbackQuery):
    # DB actions
    id_user = await get_user_id(call.message.chat.id)
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_planned']
    record = collection.find_one({"id_user": id_user})

    action = call.data.split('.')[1]

    if action == 'delete':
        status = await delete_anime_from_user_profile(record["animes"][record['page']]['target_id'],
                                                      call.message.chat.id)
        if status == 204:
            ans = f"✔️ {await translate_text(call.message, 'Anime successfully Deleted')}"
        else:
            ans = f"❌ {await translate_text(call.message, 'Anime was not Delete')}"

        await call.message.answer(ans)

    if action == 'watch':
        status = await add_anime_rate(record["animes"][record['page']]['target_id'], call.message.chat.id,
                                      'watching')

        if status == 201:
            ans = "✔️ Anime successfully added to your watching list"
        else:
            ans = "❌ Anime wasn't add to your watching list"

        await call.message.answer(ans)

    if action == 'completed':
        status = await add_anime_rate(record["animes"][record['page']]['target_id'], call.message.chat.id,
                                      'completed')

        if status == 201:
            ans = f"✔️ {await translate_text(call.message, 'Anime successfully added to your completed list')}"
        else:
            ans = f"❌ {await translate_text(call.message, 'Anime was not add to your completed list')}"

        await call.message.answer(ans)

    if action == 'back':
        await display_anime_on_message(call.message, 'anime_planned')

    await call.message.delete()


async def callback_anime_completed_edit(call: types.CallbackQuery):
    # get required datas
    id_user = await get_user_id(call.message.chat.id)
    action = call.data.split('.')[1]

    # get DB
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_completed']
    completed_animes = collection.find_one({'id_user': id_user})

    anime_with_page = completed_animes['completed_animes'][completed_animes['page']]

    if action == 'delete':
        resp = await delete_anime_from_user_profile(anime_with_page['target_id'], call.message.chat.id)
        if resp == 204:
            ans = await translate_text(call.message, 'Anime was Deleted')
        else:
            ans = await translate_text(call.message, "Anime wasn't Deleted")

        await call.message.answer(ans)

    elif action == 'back':
        await display_anime_on_message(call.message, 'anime_completed')

    else:
        await call.message.answer(await translate_text(call.message, "Write a rating 0 - 10"))
        await UpdateScoreCompleted.score.set()

    await call.message.delete()


async def paginator_for_anime_lists(call: types.CallbackQuery):
    # DB actions
    db_current = db_client['telegram-shiki-bot']

    # get collection
    coll = call.data.split('.')[1]
    collection = db_current[coll]

    # get id
    id_user = await get_user_id(call.message.chat.id)

    # get required datas
    record = collection.find_one({'id_user': id_user})
    page = record['page']
    action = call.data.split('.')[2]

    # Boring ifs
    if action == "next_1":
        if record['page'] + 1 < len(record['animes']):
            page += 1

        else:
            await call.message.answer(await translate_text(call.message, "Its last Anime in your Planned list"))
            return

    elif action == "next_5":
        if record['page'] + 5 < len(record['animes']):
            page += 5
        else:
            await call.message.answer(await translate_text(call.message, "You can't go five pages ahead"))
            return

    elif action == "prev_1":
        if record['page'] - 1 >= 0:
            page -= 1
        else:
            await call.message.answer(await translate_text(call.message, "You can't go back a page"))
            return

    elif action == "prev_5":
        if record['page'] - 5 >= 0:
            page -= 5
        else:
            await call.message.answer(await translate_text(call.message, "You can't go back a five pages"))
            return

    else:
        await display_anime_on_message(call.message, coll, is_edit=True)
        await call.message.delete()
        return

    collection.update_one({'id_user': id_user}, {"$set": {'page': page}})

    await display_anime_on_message(call.message, coll)
    await call.message.delete()


async def anime_search_callback(call: types.CallbackQuery):
    """this callback implements pagination for function anime_search_pagination"""
    action = call.data.split('.')[1]
    # Db connect
    db_current = db_client['telegram-shiki-bot']
    # get collection
    collection = db_current["anime_searchers"]
    record = collection.find_one({"chat_id": call.message.chat.id})

    if action == "next":
        if record['page'] < len(record['anime_founds']):
            collection.update_one({"chat_id": call.message.chat.id}, {"$set": {"page": record['page'] + 1}})
        else:
            await call.message.answer(await translate_text(call.message, 'Its last anime which was find'))
            return

    elif action == 'previous':
        if record['page'] > 0:
            collection.update_one({"chat_id": call.message.chat.id}, {"$set": {"page": record['page'] - 1}})
        else:
            await call.message.answer(await translate_text(call.message, 'Its first anime which was find'))
            return

    elif action == "into_planned":
        check_anime = await check_anime_already_in_profile(call.message.chat.id,
                                                           record['anime_founds'][record['page'] - 1]['id'])
        if check_anime:
            await call.message.answer(f"Anime <b>{record['anime_founds'][record['page'] - 1]['name']}</b> "
                                      f"{await translate_text(call.message, 'Already')} "
                                      f"{await translate_text(call.message, f'Exists in your {check_anime}')}",
                                      parse_mode='HTML')
            return

        # Mark anime as planned
        res = await add_anime_rate(record['anime_founds'][record['page'] - 1]['id'], call.message.chat.id,
                                   'completed')
        if res.status == 201:
            await call.message.delete()

            await call.message.answer(await translate_text(call.message, "Anime was added to planned"),
                                      parse_mode='HTML')
        # Bad request
        else:
            await call.message.answer(await translate_text(call.message, "Something went wrong"))
        return

    await anime_search_pagination(call.message)
    await call.message.delete()


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(reset_user_callback, lambda call: call.data.split('.')[0] == 'reset_user')
    dp.register_callback_query_handler(anime_search_callback, lambda call: call.data.split('.')[0] == 'anime_search')
    dp.register_callback_query_handler(callback_watch_anime_edit,
                                       lambda call: call.data.split('.')[0] == 'anime_watch_edit')

    dp.register_callback_query_handler(callback_anime_planned_edit,
                                       lambda call: call.data.split('.')[0] == 'anime_planned_edit')

    dp.register_callback_query_handler(callback_anime_completed_edit,
                                       lambda call: call.data.split('.')[0] == 'anime_completed_edit')
    dp.register_callback_query_handler(paginator_for_anime_lists, lambda call: call.data.split('.')[0] == 'paginator')