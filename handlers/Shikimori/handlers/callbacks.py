from aiogram import Dispatcher, types

from Keyboard.inline import (
    profile_manager,
    keyboard_unlink,
    unlink_manager,
)
from Keyboard.shikimori import inline
from database.database import db_repository
from database.repositories.shikimori import shiki_repository
from handlers.Shikimori.utils.shiki_api import shiki_api
from utils.message import message_work
from misc.constants import SHIKI_URL


async def unlink_user(call: types.CallbackQuery):
    """call when user press unlink his profile"""
    # check maybe already unlinked his profile
    user = await db_repository.get_one(
        filter={"chat_id": call.message.chat.id}, collection="users_id"
    )
    if not user:
        await call.message.delete()
        return

    kb = await keyboard_unlink()
    await call.message.answer(
        "Вы уверены, что хотите отвязать профиль?", reply_markup=kb
    )


async def unlink_user_db(call: types.CallbackQuery, callback_data: dict):
    """delete user from our database"""
    action = callback_data.get("action")

    if not action:
        return

    user = await db_repository.get_one(
        filter={"chat_id", call.message.chat.id}, collection="users_id"
    )

    if action == "yes" and user:
        await db_repository.delete_many(
            filter={"chat_id": call.message.chat.id}, collection="users_id"
        )
        await call.answer("Вы отвязали свой профиль!")

    await call.message.delete()


async def delete_user_rate(call: types.CallbackQuery, callback_data: dict) -> None:
    response = await shiki_api.remove_user_rate(
        callback_data.get("anime_id"), call.message.chat.id
    )
    if response.status != 200:
        await call.answer("Произошла Ошибка")
    else:
        await call.answer("Успешно удалено")


async def update_score(call: types.CallbackQuery, callback_data: dict) -> None:
    """
    update score in user rate on shikimori
    """
    response = await shiki_api.update_anime_score(
        callback_data.get("anime_id"), call.message.chat.id, callback_data.get("score")
    )
    if response.status != 200:
        await call.answer("Произошла Ошибка")

    else:
        await call.answer("Успешно Обновлено")


async def mark_anime_into_list(call: types.CallbackQuery, callback_data: dict) -> None:
    """
    mark anime into user watching list
    """
    anime_id = callback_data.get("anime_id")
    status = callback_data.get("status")
    response = await shiki_api.add_anime_rate(anime_id, call.message.chat.id, status)

    if response.status != 201:
        await call.answer("Произошла Ошибка")
    else:
        await call.answer("Успешно Обновлено")


async def update_score_message(call: types.CallbackQuery, callback_data: dict) -> None:
    """
    send message with scores 0-10
    """
    kb = await inline.score_keyboard(callback_data.get("anime_id"))
    await call.message.answer("Выберите оценку", reply_markup=kb)


async def pagination_lists(call: types.CallbackQuery, callback_data: dict) -> None:
    page = callback_data.get("page")
    collection = callback_data.get("collection")
    animes = await shiki_repository.get_shiki_list(call.message.chat.id, collection)

    kb = await inline.keyboard_anime_view(animes, collection, page)
    await call.message.edit_reply_markup(kb)


async def pagination_user_rates(call: types.CallbackQuery, callback_data: dict) -> None:
    page = callback_data.get("page")
    collection = callback_data.get("collection")
    animes = await shiki_repository.get_one(
        collection,
        {
            "chat_id": call.message.chat.id,
        },
    )
    kb = await inline.keyboard_user_rate_view(animes["animes"], collection, page)
    await call.message.edit_reply_markup(kb)


async def view_anime(call: types.CallbackQuery, callback_data: dict) -> None:
    anime_id = callback_data.get("anime_id")

    kb = await inline.shiki_keyboard(anime_id)
    anime = (await shiki_api.get_anime(anime_id)).text
    text = await message_work.anime_info_msg(anime)

    await call.message.reply_photo(
        SHIKI_URL + anime["image"]["original"], text, reply_markup=kb
    )


async def view_user_rate(call: types.CallbackQuery, callback_data: dict) -> None:
    anime_id = callback_data.get("anime_id")

    kb = await inline.shiki_user_rate_kb(anime_id)
    user_rate = await shiki_api.get_user_rate(call.message.chat.id, anime_id)
    anime = await shiki_api.get_anime(anime_id)
    text = await message_work.anime_info_rate_msg(user_rate.text[0], anime.text)
    await call.message.reply_photo(
        SHIKI_URL + anime.text["image"]["original"], text, reply_markup=kb
    )


async def episodes_mark(call: types.CallbackQuery, callback_data: dict) -> None:
    anime_id = callback_data.get("anime_id")
    anime_info = (await shiki_api.get_anime(anime_id)).text
    kb = await inline.episodes_keyboard(anime_id, anime_info.get("episodes_aired"))
    await call.message.answer(
        f"Выберите последний просмотренный вами эпизод - {anime_info['russian']}",
        reply_markup=kb,
    )


async def pagination_episodes(call: types.CallbackQuery, callback_data: dict) -> None:
    anime_id = callback_data.get("anime_id")
    page = callback_data.get("page")
    anime_info = (await shiki_api.get_anime(anime_id)).text
    kb = await inline.episodes_keyboard(
        anime_id, anime_info.get("episodes_aired"), page
    )
    await call.message.edit_reply_markup(kb)


async def mark_episode(call: types.CallbackQuery, callback_data: dict) -> None:
    anime_id = callback_data.get("anime_id")
    episode = callback_data.get("episode")

    resp = await shiki_api.update_anime_episodes(
        anime_id, call.message.chat.id, episode
    )

    if resp.status == 200:
        await call.answer("Успешно Обновлено")

    else:
        await call.answer("Произошла Ошибка")


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(view_anime, inline.anime_view.filter())
    dp.register_callback_query_handler(view_user_rate, inline.user_rate_view.filter())
    dp.register_callback_query_handler(episodes_mark, inline.episode_start_clk.filter())
    dp.register_callback_query_handler(
        pagination_episodes, inline.pagination_episode.filter()
    )
    dp.register_callback_query_handler(mark_episode, inline.episode_clk.filter())
    dp.register_callback_query_handler(
        unlink_user, profile_manager.filter(action="unlink")
    )
    dp.register_callback_query_handler(unlink_user_db, unlink_manager.filter())

    dp.register_callback_query_handler(
        pagination_lists, inline.pagination_anime.filter()
    )
    dp.register_callback_query_handler(
        pagination_user_rates, inline.pagination_user_rate.filter()
    )
    dp.register_callback_query_handler(update_score, inline.update_score_clk.filter())
    dp.register_callback_query_handler(
        mark_anime_into_list, inline.user_lists_clk.filter()
    )
    dp.register_callback_query_handler(
        update_score_message,
        inline.update_score.filter(),
    )
    dp.register_callback_query_handler(
        delete_user_rate, inline.delete_from_list_clk.filter()
    )
