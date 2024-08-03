from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.enums import ShikimoriListType


class ShikimoriUpdateEpisode(CallbackData, prefix="shikimori_update_episode"):
    episode: int
    id: int


class ReturnToShikimoriList(CallbackData, prefix="return_to_shikimori_list"):
    type: ShikimoriListType
    page: int


class ShikimoriEpisodePagination(CallbackData, prefix="shikimori_episode_pagination"):
    id: int
    page: int = 0
    last_episode: int


class ShikimoriEpisodePaginationStart(
    CallbackData, prefix="shikimori_episode_pagination_start"
):
    id: int
    page: int = 0
    last_episode: int


class ShikimoriEditStatus(CallbackData, prefix="shikimori_edit_status"):
    status: ShikimoriListType
    id: int


class ShikimoriViewTitle(CallbackData, prefix="shikimori_view_title"):
    id: int


class ShikimoriDeleteTitle(CallbackData, prefix="shikimori_delete_title"):
    id: int


class ReturnToEditTitle(CallbackData, prefix="return_to_edit_title"):
    type: ShikimoriListType
    user_rate_page: int
    id: int


def return_to_edit_title_btn(
    id: int, type: ShikimoriListType, user_rate_page: int
) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=" <- Вернуться",
        callback_data=ReturnToEditTitle(
            id=id, type=type, user_rate_page=user_rate_page
        ).pack(),
    )


def _completed_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Просмотрено",
        callback_data=ShikimoriEditStatus(
            id=id, status=ShikimoriListType.COMPLETED
        ).pack(),
    )


def _watch_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Смотрю",
        callback_data=ShikimoriEditStatus(
            id=id, status=ShikimoriListType.WATCHING
        ).pack(),
    )


def _rewatch_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Пересматриваю",
        callback_data=ShikimoriEditStatus(
            id=id, status=ShikimoriListType.REWATCHING
        ).pack(),
    )


def _dropped_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Брошено",
        callback_data=ShikimoriEditStatus(
            id=id, status=ShikimoriListType.DROPPED
        ).pack(),
    )


def _on_hold_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Отложено",
        callback_data=ShikimoriEditStatus(
            id=id, status=ShikimoriListType.ON_HOLD
        ).pack(),
    )


def _planned_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Запланировано",
        callback_data=ShikimoriEditStatus(
            id=id, status=ShikimoriListType.PLANNED
        ).pack(),
    )


def _delete_btn(id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Удалить",
        callback_data=ShikimoriDeleteTitle(id=id).pack(),
    )


def _mark_episode(id: int, last_episode: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="Отметить Эпизод",
        callback_data=ShikimoriEpisodePaginationStart(
            last_episode=last_episode, id=id
        ).pack(),
    )


def edit_user_rate_keyboard(
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
    )

    kb.button(
        text="Вернуться",
        callback_data=ReturnToShikimoriList(page=page, type=list_type),
    )

    return kb.adjust(1, 2).as_markup()


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
    )

    return kb.adjust(1, 2).as_markup()


def episode_keyboard(id: int, page: int, last_episode: int) -> InlineKeyboardMarkup:
    """
    This function represents a keyboard with update concrete episode on concrete anime.

    Available actions:
    - edit episodes
    - pagination on episodes

    """
    builder = InlineKeyboardBuilder()

    for i in range(page, page + 30):
        builder.button(
            text=f"{i}", callback_data=ShikimoriUpdateEpisode(episode=i, id=id)
        )
        if i == last_episode:
            break

    # pagination buttons
    if page > 1:
        builder.button(
            text="<<",
            callback_data=ShikimoriEpisodePagination(
                id=id, page=page - 30, last_episode=last_episode
            ).pack(),
        )
    if page + 30 < last_episode:
        builder.button(
            text=">>",
            callback_data=ShikimoriEpisodePagination(
                id=id, page=page + 30, last_episode=last_episode
            ).pack(),
        )

    return builder.adjust().as_markup()
