from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Keyboard.reply import keyboard_status, default_keyboard
from bot import anilibria_client
from database.database import db_repository
from handlers.Shikimori.shikimori_requests import ShikimoriRequests


class AnimeFollow(StatesGroup):
    anime_title = State()


class AnimeMarkShiki(StatesGroup):
    status = State()
    eps = State()


class AnimeGetTorrent(StatesGroup):
    title = State()


async def start_shiki_mark_from_al(message: types.Message, eps):
    await message.answer(f"Укажите число эпизодов, их всего - {eps}.")
    await AnimeMarkShiki.eps.set()


async def get_eps_set_status(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["eps"] = message.text

    await AnimeMarkShiki.status.set()
    await message.answer(
        "Укажите статус выбранного вами аниме.", reply_markup=keyboard_status
    )


async def finish_AnimeMarkShiki(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        record = await db_repository.get_one(
            {"chat_id": message.chat.id}, collection="shiki_mark_from_al"
        )

        st = await ShikimoriRequests.AddAnimeRate(
            record["anime"], message.chat.id, message.text, data["eps"]
        )
        await state.finish()
        if st == 201:
            await message.answer(
                "✅ Аниме было добавлено в ваш профиль на Shikimori.",
                reply_markup=default_keyboard,
            )
        else:
            await message.answer(
                "❌ Что-то пошло не так, попробуйте еще раз.",
                reply_markup=default_keyboard,
            )


async def start_get_torrent(message: types.Message):
    await message.answer(
        f"Напиши названия тайтла, а я поищу его.\n" f"Можете отменить - /cancel."
    )
    await AnimeGetTorrent.title.set()


async def get_torrent_title(message: types.Message, state: FSMContext):
    await state.finish()
    animes = await anilibria_client.search_titles([message.text])

    kb = InlineKeyboardMarkup()
    for anime in animes.list:
        kb.add(
            InlineKeyboardButton(
                text=f"{anime.names.ru}", callback_data=f"{anime.id}.get_torrent"
            )
        )

    kb.add(InlineKeyboardButton(text=f"❌ Cancel", callback_data="cancel.get_torrent"))

    await message.bot.send_photo(
        message.chat.id,
        open("misc/img/pic2.png", "rb"),
        reply_markup=kb,
        caption=f"Нажмите на интересующее вас аниме, чтобы получить торрент файл.",
    )


def register_states_anilibria(dp: Dispatcher):
    dp.register_message_handler(get_eps_set_status, state=AnimeMarkShiki.eps)
    dp.register_message_handler(finish_AnimeMarkShiki, state=AnimeMarkShiki.status)
    dp.register_message_handler(get_torrent_title, state=AnimeGetTorrent.title)