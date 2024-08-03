from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.telegram.common.keyboards.cancel import cancel_btn
from src.presentation.telegram.common.keyboards.shikimori.user_rate import (
    _completed_btn,
    _dropped_btn,
    _planned_btn,
    _rewatch_btn,
    _on_hold_btn,
    _watch_btn,
    _mark_episode,
)


class ShikimoriViewTitle(CallbackData, prefix="shikimori_view_title"):
    id: int


def edit_title_keyboard(id: int, last_episode: int):
    kb = InlineKeyboardBuilder()
    kb.add(
        _completed_btn(id),
        _dropped_btn(id),
        _planned_btn(id),
        _rewatch_btn(id),
        _on_hold_btn(id),
        _watch_btn(id),
        _mark_episode(id, last_episode),
        cancel_btn(),
    )

    return kb.adjust(1, 2).as_markup()
