from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .lists import user_list_return_button
from src.application.enums import ShikimoriListType

class EpisodeEditCallback(CallbackData, prefix="episode_edit_callback"):
    episode: int
    id: int


class EpisodePaginationCallback(CallbackData, prefix="episode_pagination_callback"):
    page: int = 0
    last_episode: int


class ReturnEditTitleCallback(CallbackData, prefix="return_edit_title_callback"):
    id: int




class MarkStatusTitleCallback(CallbackData, prefix="mark_status_title_callback"):
    status: str  # todo enums
    id: int


def info_keyboard(type: ShikimoriListType, page: int, id: int) -> InlineKeyboardMarkup:
    return_btn = user_list_return_button(page, type)
    # todo кнопки редактирования


def episode_keyboard() -> InlineKeyboardMarkup:
    pass




