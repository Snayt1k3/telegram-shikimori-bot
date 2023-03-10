from aiogram import Dispatcher, types

from bot import dp, db_client
from .helpful_functions import get_information_from_anime, get_user_id, delete_anime_from_user_profile, add_anime_rate, \
    update_anime_eps, get_anime_info_user_rate
from .states import UpdateScore, UpdateScoreCompleted
from .shikimori_profile import pagination_watching_list, paginator_completed_list, paginator_planned_list

async def reset_user_callback(call):
    data = call.data.split(".")[1]
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    if data == "True":
        # Db connect
        db_current = db_client['telegram-shiki-bot']
        # get collection
        collection = db_current["ids_users"]
        collection.delete_one({'chat_id': call.message.chat.id})
        await dp.bot.send_message(call.message.chat.id, "Deleted")
    else:
        await dp.bot.send_message(call.message.chat.id, "❌ Cancelled")


async def anime_watch_callback(call):
    """This method implements pagination for watch_list"""
    # DB actions
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_watch_list']
    watch_list = collection.find_one({"chat_id": call.message.chat.id})
    # Get action, for next actions
    action = call.data.split('.')[1]

    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)

    if action == 'next':
        # Here check current page, if page out of limit, send a warning message
        if len(watch_list['anime_target_ids']) > watch_list['page'] + 1:
            collection.update_one({"chat_id": call.message.chat.id}, {"$set": {"page": watch_list['page'] + 1}})
            await pagination_watching_list(call.message)
        else:
            await pagination_watching_list(call.message)
            await dp.bot.send_message(call.message.chat.id, "It's last Anime")

    # As well as in action next
    elif action == 'previous':
        if watch_list['page'] > 0:
            collection.update_one({"chat_id": call.message.chat.id}, {"$set": {"page": watch_list['page'] - 1}})
            await pagination_watching_list(call.message)
        else:
            await pagination_watching_list(call.message)
            await dp.bot.send_message(call.message.chat.id, "It's first anime")

    # Here call pagination with is_edit=True
    else:
        await pagination_watching_list(call.message, is_edit=True)


async def callback_watch_anime_edit(call):
    """This callback realize anime from watch_list edit"""
    # DB actions
    db_current = db_client['telegram-shiki-bot']

    # Change collection, for actions on anime
    collection = db_current['anime_watch_list']

    # Find user watch_list
    watch_list = collection.find_one({"chat_id": call.message.chat.id})

    action = call.data.split(".")[1]

    if action == 'back':
        await pagination_watching_list(call.message, is_edit=False)

    if action == 'delete':
        # Here make a request(DELETE), delete from watch_list
        status = await delete_anime_from_user_profile(watch_list['anime_target_ids'][watch_list['page']],
                                                      call.message.chat.id)
        if status == 204:
            await dp.bot.send_message(call.message.chat.id, "✔️ Anime was deleted")
        else:
            await dp.bot.send_message(call.message.chat.id, "❌️ Anime not deleted")

    if action == 'minus' or action == 'add':
        # get anime data and curr episode
        ep = await get_anime_info_user_rate(call.message.chat.id, watch_list['anime_target_ids'][watch_list['page']])
        ep = ep[0]['episodes']

        # make actions with episode
        if action == 'minus':
            ep -= 1

        elif action == 'add':
            ep += 1

        # make a patch request, for update count episode
        res = await update_anime_eps(watch_list['anime_target_ids'][watch_list['page']], call.message.chat.id, ep)

        if res:
            await pagination_watching_list(call.message, is_edit=True)
            await dp.bot.send_message(call.message.chat.id, f"✔️ Anime Updated, current eps - {res['episodes']}")

        else:
            await dp.bot.send_message(call.message.chat.id, '❌ Something went wrong')

    if action == 'complete':
        anime_info = await get_information_from_anime(watch_list['anime_target_ids'][watch_list['page']])
        status = await add_anime_rate(watch_list['anime_target_ids'][watch_list['page']], call.message.chat.id,
                                      'completed', episodes=anime_info['episodes'])

        if status == 201:
            await dp.bot.send_message(call.message.chat.id, "✔️ Anime was Updated")
            await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
            return

        else:
            await dp.bot.send_message(call.message.chat.id, '❌ Something went wrong')

    if action == 'update_score':
        await dp.bot.send_message(call.message.chat.id, "Write an anime score 1-10")
        await UpdateScore.score.set()

    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)


async def callback_planned_list(call):
    """This callback Provides work function paginator_planned_list"""
    # DB actions
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_planned']
    record = collection.find_one({"chat_id": call.message.chat.id})

    # get require datas
    page = record['page']
    action = call.data.split('.')[1]

    # Boring ifs
    if action == "next_1":
        if record['page'] + 1 < len(record['animes']):
            page += 1

        else:
            await dp.bot.send_message(call.message.chat.id, "Its last Anime in your Planned list")
            return

    elif action == "next_5":
        if record['page'] + 5 < len(record['animes']):
            page += 5
        else:
            await dp.bot.send_message(call.message.chat.id, "You can't go five pages ahead")
            return

    elif action == "prev_1":
        if record['page'] - 1 > 0:
            page -= 1
        else:
            await dp.bot.send_message(call.message.chat.id, "You can't go back a page")
            return

    elif action == "prev_5":
        if record['page'] - 5 > 0:
            page -= 5
        else:
            await dp.bot.send_message(call.message.chat.id, "You can't go back a five pages")
            return

    else:
        await paginator_planned_list(call.message, is_edit=True)
        await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
        return

    collection.update_one({'chat_id': call.message.chat.id}, {"$set": {'page': page}})
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    await paginator_planned_list(call.message)


async def callback_anime_planned_edit(call):
    # DB actions
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_planned']
    record = collection.find_one({"chat_id": call.message.chat.id})

    action = call.data.split('.')[1]

    if action == 'delete':
        status = await delete_anime_from_user_profile(record["animes"][record['page']]['target_id'],
                                                      call.message.chat.id)
        if status == 204:
            ans = "✔️ Anime successfully Deleted"
        else:
            ans = "❌ Anime wasn't Delete"

        await dp.bot.send_message(call.message.chat.id, ans)

    if action == 'watch':
        status = await add_anime_rate(record["animes"][record['page']]['target_id'], call.message.chat.id,
                                      'watching')

        if status == 201:
            ans = "✔️ Anime successfully added to your watching list"
        else:
            ans = "❌ Anime wasn't add to your watching list"

        await dp.bot.send_message(call.message.chat.id, ans)

    if action == 'completed':
        status = await add_anime_rate(record["animes"][record['page']]['target_id'], call.message.chat.id,
                                      'completed')

        if status == 201:
            ans = "✔️ Anime successfully added to your completed list"
        else:
            ans = "❌ Anime wasn't add to your completed list"

        await dp.bot.send_message(call.message.chat.id, ans)

    if action == 'back':
        await paginator_planned_list(call.message)

    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)


async def callback_completed_pagination(call):
    id_user = await get_user_id(call.message.chat.id)
    # DB actions
    db_current = db_client['telegram-shiki-bot']
    collection = db_current['anime_completed']
    record = collection.find_one({"id_user": id_user})

    # get required datas
    page = record['page']
    action = call.data.split('.')[1]

    # Boring ifs
    if action == "next_1":
        if record['page'] + 1 < len(record['completed_animes']):
            page += 1

        else:
            await dp.bot.send_message(call.message.chat.id, "Its last Anime in your Planned list")
            return

    elif action == "next_5":
        if record['page'] + 5 < len(record['completed_animes']):
            page += 5
        else:
            await dp.bot.send_message(call.message.chat.id, "You can't go five pages ahead")
            return

    elif action == "prev_1":
        if record['page'] - 1 > 0:
            page -= 1
        else:
            await dp.bot.send_message(call.message.chat.id, "You can't go back a page")
            return

    elif action == "prev_5":
        if record['page'] - 5 > 0:
            page -= 5
        else:
            await dp.bot.send_message(call.message.chat.id, "You can't go back a five pages")
            return

    else:
        await paginator_completed_list(call.message, is_edit=True)
        await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
        return

    collection.update_one({'id_user': id_user}, {"$set": {'page': page}})
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    await paginator_completed_list(call.message)


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
            ans = 'Anime was Deleted'
        else:
            ans = "Anime wasn't Deleted"

        await dp.bot.send_message(call.message.chat.id, ans)

    elif action == 'back':
        await paginator_completed_list(call.message)

    else:
        await dp.bot.send_message(call.message.chat.id, "Write a rating 0 - 10")
        await UpdateScoreCompleted.score.set()

    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(reset_user_callback, lambda call: call.data.split('.')[0] == 'reset_user')

    dp.register_callback_query_handler(anime_watch_callback, lambda call: call.data.split('.')[0] == 'anime_watch')
    dp.register_callback_query_handler(callback_watch_anime_edit,
                                       lambda call: call.data.split('.')[0] == 'anime_watch_one')

    dp.register_callback_query_handler(callback_planned_list, lambda call: call.data.split('.')[0] == 'anime_planned')
    dp.register_callback_query_handler(callback_anime_planned_edit,
                                       lambda call: call.data.split('.')[0] == 'anime_planned_edit')

    dp.register_callback_query_handler(callback_completed_pagination,
                                       lambda call: call.data.split('.')[0] == 'anime_completed')
    dp.register_callback_query_handler(callback_anime_completed_edit,
                                       lambda call: call.data.split('.')[0] == 'anime_completed_edit')
