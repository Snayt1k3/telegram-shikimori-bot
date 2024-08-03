from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.telegram.common.constants import EPISODE_PAGINATION
from src.presentation.telegram.common.keyboards.cancel import cancel_btn


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


class ShikimoriUpdateEpisode(CallbackData, prefix="shikimori_update_episode"):
    episode: int
    id: int


def episode_keyboard(id: int, page: int, last_episode: int) -> InlineKeyboardMarkup:
    """
    This function represents a keyboard with update concrete episode on concrete anime.

    Available actions:
    - edit episodes
    - pagination on episodes

    """
    builder = InlineKeyboardBuilder()

    for i in range(page, page + EPISODE_PAGINATION):
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
                id=id, page=page - EPISODE_PAGINATION, last_episode=last_episode
            ).pack(),
        )
    if page + EPISODE_PAGINATION < last_episode:
        builder.button(
            text=">>",
            callback_data=ShikimoriEpisodePagination(
                id=id, page=page + EPISODE_PAGINATION, last_episode=last_episode
            ).pack(),
        )
    builder.row(cancel_btn())
    return builder.adjust().as_markup()
