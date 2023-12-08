from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from database.schemas.animes import ShikimoriAnime


planned_list_clk = CallbackData("planned_list", "anime_id")
completed_list_clk = CallbackData("completed_list", "anime_id")
dropped_list_clk = CallbackData("dropped_list", "anime_id")
watching_list_clk = CallbackData("watching_list", "anime_id")

delete_from_list_clk = CallbackData("delete_from_list", "anime_id")

cancel_clk = CallbackData("cancel")

mark_episode_clk = CallbackData("episode_mark", "episode", "anime_id")

pagination_clk = CallbackData("pagination", "collection", "page")

anime_view = CallbackData("anime_view", "anime_id")
user_rate_view = CallbackData("user_rate_view", "anime_id")


async def keyboard_anime_view(animes: list[ShikimoriAnime]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    for anime in animes:
        kb.add(InlineKeyboardButton(anime.title_ru, callback_data=anime_view.new(anime_id=anime.id)))

    kb.add(InlineKeyboardButton("cancel ❌", callback_data=cancel_clk.new()))

    return kb


async def keyboard_user_rate_view(animes: list[ShikimoriAnime]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    for anime in animes:
        kb.add(InlineKeyboardButton(anime.title_ru, callback_data=user_rate_view.new(anime_id=anime.id)))

    kb.add(InlineKeyboardButton("cancel ❌", callback_data=cancel_clk.new()))

    return kb
