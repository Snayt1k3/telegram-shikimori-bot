from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.telegram.common.keyboards.torrent import TorrentCallback
from src.presentation.telegram.common.keyboards.user import follows


class AnilibriaTitle(CallbackData, prefix="anilibria_title"):
    id: int


def anilibria_title_kb(id: int) -> types.InlineKeyboardMarkup:
    """
    Keyboard for action with anime from anilibria.api

    Available actions:
    - follow/unfollow
    - torrent
    - search on shikimori by name
    """
    builder = InlineKeyboardBuilder()

    builder.button(text="🔔 Подписаться", callback_data=follows.Follow(id=id).pack())
    builder.button(text="🔕 Отписаться", callback_data=follows.UnFollow(id=id).pack())
    builder.button(text="💾 Торрент", callback_data=TorrentCallback(id=id).pack())

    return builder.adjust(2).as_markup()
