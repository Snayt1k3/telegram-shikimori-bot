from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from database.schemas.animes import AnilibriaAnime

all_follows_clk = CallbackData("all_follows", "anime_id", "page")
all_follows_back = CallbackData("all_follows_back", "page")
all_follows_pagination = CallbackData("all_follows_pagination", "page", "action")

search_anilibria_clk = CallbackData("search_anilibria", "anime_id")
search_anilibria_back_clk = CallbackData("search_anilibria_back")

search_shikimori_start_clk = CallbackData("search_shikimori_start", "anime_id")
search_shikimori_clk = CallbackData("search_shikimori", "anime_id")
search_shikimori_back_clk = CallbackData("search_shikimori_back")

anime_follow_clk = CallbackData("anime_follow", "anime_id", "action")
torrent_clk = CallbackData("torrent_anilibria", "anime_id")

cancel_clk = CallbackData("cancel")


async def all_follows_kb(follows: list, page=0) -> InlineKeyboardMarkup:
    """
    keyboard display anime in reply_markup and implements pagination
    """

    kb = InlineKeyboardMarkup()

    for anime in follows[page : page + 8]:
        kb.add(
            InlineKeyboardButton(
                anime.title_ru,
                callback_data=all_follows_clk.new(anime_id=anime.id, page=page),
            )
        )

    # add pagination buttons response by current page
    if len(follows) > page + 8 and page > 0:
        kb.add(
            InlineKeyboardButton(
                text="<<",
                callback_data=all_follows_pagination.new(action="prev", page=page),
            ),
            InlineKeyboardButton(
                text=">>",
                callback_data=all_follows_pagination.new(action="next", page=page),
            ),
        )

    elif len(follows) > page + 8:
        kb.add(
            InlineKeyboardButton(
                text=">>",
                callback_data=all_follows_pagination.new(action="next", page=page),
            ),
        )

    elif page > 0:
        kb.add(
            InlineKeyboardButton(
                text="<<",
                callback_data=all_follows_pagination.new(action="prev", page=page),
            )
        )

    return kb


async def all_follows_edit_kb(anime_id: int | str, page: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    back = InlineKeyboardButton("⬅", callback_data=all_follows_back.new(page=page))
    unfollow = InlineKeyboardButton(
        "💔", callback_data=anime_follow_clk.new(anime_id=anime_id, action="unfollow")
    )
    mark_on_shiki = InlineKeyboardButton(
        "📌 Шикимори", callback_data=search_shikimori_start_clk.new(anime_id=anime_id)
    )
    get_torrent = InlineKeyboardButton(
        "⬇ torrent", callback_data=torrent_clk.new(anime_id=anime_id)
    )
    kb.add(back, unfollow, mark_on_shiki, get_torrent)
    return kb


async def animes_from_shikimori_kb(animes: list[dict]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    for anime in animes:
        kb.add(
            InlineKeyboardButton(
                anime["russian"],
                callback_data=search_shikimori_clk.new(anime_id=anime["id"]),
            )
        )
    kb.add(
        InlineKeyboardButton("❌ Cancel", callback_data=cancel_clk.new()),
    )
    return kb


async def search_anime_kb(animes: list[AnilibriaAnime]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    for anime in animes:
        kb.add(
            InlineKeyboardButton(
                anime.title_ru,
                callback_data=search_anilibria_clk.new(anime_id=anime.id),
            )
        )

    kb.add(InlineKeyboardButton("❌ Cancel", callback_data=cancel_clk.new()))
    return kb


async def search_actions_keyboard(anime_id: int | str) -> InlineKeyboardMarkup:
    search_kb = InlineKeyboardMarkup(row_width=4)
    back = InlineKeyboardButton("⬅", callback_data=search_anilibria_back_clk.new())
    follow_btn = InlineKeyboardButton(
        "❤️ Подписаться",
        callback_data=anime_follow_clk.new(anime_id=anime_id, action="follow"),
    )
    mark_on_shiki = InlineKeyboardButton(
        "📌 Шикимори", callback_data=search_shikimori_start_clk.new(anime_id=anime_id)
    )
    get_torrent = InlineKeyboardButton(
        "⬇ torrent", callback_data=torrent_clk.new(anime_id=anime_id)
    )
    search_kb.add(back, follow_btn).add(mark_on_shiki, get_torrent)
    return search_kb


async def shikimori_mark_actions_kb(anime_id: int | str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(
            "✔️ Просмотрено", callback_data=f"completed.{anime_id}.shiki_mark_action"
        ),
        InlineKeyboardButton(
            "🎥 Смотрю", callback_data=f"watching.{anime_id}.shiki_mark_action"
        ),
        InlineKeyboardButton(
            "🗑 Брошено", callback_data=f"dropped.{anime_id}.shiki_mark_action"
        ),
        InlineKeyboardButton(
            "📝 Запланированное", callback_data=f"planned.{anime_id}.shiki_mark_action"
        ),
        InlineKeyboardButton(
            "✏️ Оценка", callback_data=f"score.{anime_id}.shiki_mark_action"
        ),
        InlineKeyboardButton(
            "🗑 Удалить", callback_data=f"delete.{anime_id}.shiki_mark_action"
        ),
        InlineKeyboardButton("⬅", callback_data=search_shikimori_back_clk.new()),
    ]
    kb.add(*buttons)
    return kb


async def torrent_kb(animes: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for anime in animes.list:
        kb.add(
            InlineKeyboardButton(
                text=f"{anime.names.ru}",
                callback_data=torrent_clk.new(anime_id=anime.id),
            )
        )

    kb.add(InlineKeyboardButton(text=f"❌ Cancel", callback_data=cancel_clk.new()))
    return kb
