from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.enums import ShikimoriListType
from src.presentation.telegram.common.keyboards.cancel import cancel_btn
from src.presentation.telegram.common.keyboards.shikimori.episode import (
    ShikimoriEpisodePaginationStart,
)


class ShikimoriDeleteUserRate(CallbackData, prefix="shikimori_delete_title"):
    id: int


class ShikimoriUpdateStatus(CallbackData, prefix="shikimori_edit_status"):
    status: ShikimoriListType
    id: int


class ReturnToUserRatesList(CallbackData, prefix="return_to_shikimori_list"):
    type: ShikimoriListType
    page: int


def _completed_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Просмотрено/Прочитано",
        callback_data=ShikimoriUpdateStatus(
            id=id, status=ShikimoriListType.COMPLETED
        ).pack(),
    )


def _watch_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Смотрю/Читаю",
        callback_data=ShikimoriUpdateStatus(
            id=id, status=ShikimoriListType.WATCHING
        ).pack(),
    )


def _rewatch_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Пересматриваю/Перечитываю",
        callback_data=ShikimoriUpdateStatus(
            id=id, status=ShikimoriListType.REWATCHING
        ).pack(),
    )


def _dropped_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Брошено",
        callback_data=ShikimoriUpdateStatus(
            id=id, status=ShikimoriListType.DROPPED
        ).pack(),
    )


def _on_hold_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Отложено",
        callback_data=ShikimoriUpdateStatus(
            id=id, status=ShikimoriListType.ON_HOLD
        ).pack(),
    )


def _planned_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Запланировано",
        callback_data=ShikimoriUpdateStatus(
            id=id, status=ShikimoriListType.PLANNED
        ).pack(),
    )


def _delete_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Удалить 🗑",
        callback_data=ShikimoriDeleteUserRate(id=id).pack(),
    )


def _mark_episode(id: int, last_episode: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Отметить Эпизод 🏷",
        callback_data=ShikimoriEpisodePaginationStart(
            last_episode=last_episode, id=id
        ).pack(),
    )


def edit_user_rate_anime_keyboard(
    id: int, last_episode: int, page: int = 0, list_type: ShikimoriListType = None
) -> InlineKeyboardMarkup:
    """
    This function represents a keyboard with edit anime.

    Available actions:
    - edit status
    - edit episodes

    """
    kb = InlineKeyboardBuilder()
    kb.add(
        _completed_btn(id),
        _dropped_btn(id),
        _planned_btn(id),
        _rewatch_btn(id),
        _on_hold_btn(id),
        _watch_btn(id),
        _mark_episode(id, last_episode),
        _delete_btn(id),
        cancel_btn(),
    )

    kb.button(
        text="Вернуться",
        callback_data=ReturnToUserRatesList(page=page, type=list_type),
    )

    return kb.adjust(1, 2).as_markup()


def edit_user_rate_manga_keyboard(
    id: int, page: int = 0, list_type: ShikimoriListType = None
) -> InlineKeyboardMarkup:
    """
    This function represents a keyboard with edit manga.

    Available actions:
    - edit status

    """
    kb = InlineKeyboardBuilder()
    kb.add(
        _completed_btn(id),
        _dropped_btn(id),
        _planned_btn(id),
        _rewatch_btn(id),
        _on_hold_btn(id),
        _watch_btn(id),
        _delete_btn(id),
        cancel_btn(),
    )

    kb.button(
        text="Вернуться",
        callback_data=ReturnToUserRatesList(page=page, type=list_type),
    )

    return kb.adjust(1, 2).as_markup()
