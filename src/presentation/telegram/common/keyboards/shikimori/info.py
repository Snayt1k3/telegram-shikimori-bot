from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.application.enums import ShikimoriListType


class ShikimoriUpdateEpisode(CallbackData, prefix="shikimori_update_episode"):
    episode: int
    id: int


class ShikimoriEpisodePagination(CallbackData, prefix="shikimori_episode_pagination"):
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


def edit_title_keyboard(id: int, last_episode: int) -> InlineKeyboardMarkup:
    """
    This function represents a keyboard with edit anime.

    Available actions:
    - edit status
    - edit episodes

    """
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text="Просмотрено",
            callback_data=ShikimoriEditStatus(
                id=id, status=ShikimoriListType.COMPLETED
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Смотрю",
            callback_data=ShikimoriEditStatus(
                id=id, status=ShikimoriListType.WATCHING
            ).pack(),
        ),
    )
    kb.row(
        InlineKeyboardButton(
            text="Пересматриваю",
            callback_data=ShikimoriEditStatus(
                id=id, status=ShikimoriListType.REWATCHING
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Брошено",
            callback_data=ShikimoriEditStatus(
                id=id, status=ShikimoriListType.DROPPED
            ).pack(),
        ),
    )
    kb.row(
        InlineKeyboardButton(
            text="Отложено",
            callback_data=ShikimoriEditStatus(
                id=id, status=ShikimoriListType.ON_HOLD
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Запланировано",
            callback_data=ShikimoriEditStatus(
                id=id, status=ShikimoriListType.PLANNED
            ).pack(),
        ),
    )
    kb.row(
        InlineKeyboardButton(
            text="Отметить Эпизод",
            callback_data=ShikimoriEpisodePagination(
                last_episode=last_episode, id=id
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Удалить ",
            callback_data=ShikimoriDeleteTitle(id=id).pack(),
        ),
    )
    return kb.as_markup()


def episode_keyboard(id: int, page: int, last_episode: int) -> InlineKeyboardMarkup:
    """
    This function represents a keyboard with update concrete episode on concrete anime.

    Available actions:
    - edit episodes
    - pagination on episodes

    """
    builder = InlineKeyboardBuilder()

    for i in range(page * 30, page * 30 + 30):
        if i == last_episode:
            break

        builder.button(
            text=f"{i}", callback_data=ShikimoriUpdateEpisode(episode=i, id=id)
        )

    # pagination buttons
    if page > 1:
        builder.button(
            text="<<",
            callback_data=ShikimoriEpisodePagination(
                id=id, page=page - 1, last_episode=last_episode
            ).pack(),
        )
    if page * 30 < last_episode:
        builder.button(
            text=">>",
            callback_data=ShikimoriEpisodePagination(
                id=id, page=page + 1, last_episode=last_episode
            ).pack(),
        )

    return builder.as_markup()
