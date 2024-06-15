from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton


class TorrentCallback(CallbackData, prefix="torrent"):
    id: int


def torrent_button(id: int) -> InlineKeyboardButton:
    btn = InlineKeyboardButton(text="Торрент", callback_data=TorrentCallback(id=id).pack())
    return btn
