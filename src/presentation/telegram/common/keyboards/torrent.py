from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class TorrentCallback(CallbackData, prefix="torrent"):
    id: int


def torrent_button(id: int) -> InlineKeyboardButton:
    btn = InlineKeyboardButton(text="Торрент", callback_data=TorrentCallback(id=id).pack())
    return btn

def torrent_keyboard(titles: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for title in titles:
        kb.button(text=title.ru, callback_data=TorrentCallback(id=title.id).pack())

    return kb.as_markup()
