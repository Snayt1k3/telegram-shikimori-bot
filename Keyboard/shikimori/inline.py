from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


planned_list_clk = CallbackData("planned_list", "anime_id")
completed_list_clk = CallbackData("completed_list", "anime_id")
dropped_list_clk = CallbackData("dropped_list", "anime_id")
watching_list_clk = CallbackData("watching_list", "anime_id")

delete_from_list_clk = CallbackData("delete_from_list", "anime_id")

cancel_clk = CallbackData("cancel")

mark_episode_clk = CallbackData("episode_mark", "episode", "anime_id")

pagination_clk = CallbackData("pagination", "collection", "page")

