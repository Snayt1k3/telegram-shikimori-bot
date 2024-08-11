from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.telegram.common.keyboards.torrent import TorrentCallback


class AnilibriaTitle(CallbackData, prefix="anilibria_title"):
    id: int


class AnilibriaFollow(CallbackData, prefix="anilibria_follow"):
    id: int


class AnilibriaUnFollow(CallbackData, prefix="anilibria_un_follow"):
    id: int


class SearchOnShikimoriFromAnilibria(
    CallbackData, prefix="search_on_shikimori_from_anilibria"
):
    id: int
    name: str


def anilibria_title_kb(id: int, name: str) -> types.InlineKeyboardMarkup:
    """
    Keyboard for action with anime from anilibria.api

    Available actions:
    - follow/unfollow
    - torrent
    - search on shikimori by name
    """
    builder = InlineKeyboardBuilder()

    builder.button(text="🔔 Подписаться", callback_data=AnilibriaFollow(id=id).pack())
    builder.button(text="🔕 Отписаться", callback_data=AnilibriaUnFollow(id=id).pack())
    builder.button(
        text="🔍 Поиск на шикимори",
        callback_data=SearchOnShikimoriFromAnilibria(id=id, name=name).pack(),
    )
    builder.button(text="💾 Торрент", callback_data=TorrentCallback(id=id).pack())

    return builder.as_markup()
