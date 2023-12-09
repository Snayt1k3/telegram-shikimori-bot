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


class AnimeGetTorrent(StatesGroup):
    title = State()


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
    dp.register_message_handler(get_torrent_title, state=AnimeGetTorrent.title)
