from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from database.schemas.animes import AnilibriaAnime

all_follows_clk = CallbackData("all_follows", "anime_id")
all_follows_pagination = CallbackData("all_follows_pagination", "page", "action")

search_anilibria_clk = CallbackData("search_anilibria", "anime_id")
search_anilibria_back_clk = CallbackData("search_anilibria_back", "anime_id")

search_shikimori_clk = CallbackData("search_shikimori", "anime_id")
search_shikimori_back_clk = CallbackData("search_shikimori_back")


cancel_clk = CallbackData("cancel")


async def all_follows_kb(follows, action=None, page=0) -> InlineKeyboardMarkup:
    match action:
        case "-":
            page -= 8
        case "+":
            page += 8

    kb = InlineKeyboardMarkup()

    for anime in follows[page : page + 8]:
        kb.add(
            InlineKeyboardButton(
                anime.title_ru, callback_data=all_follows_clk.new(anime_id=anime.id)
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
        InlineKeyboardButton("⬅", callback_data=search_shikimori_back_clk.new()),
        InlineKeyboardButton("❌ Cancel", callback_data=cancel_clk.new()),
    )
    return kb


async def search_actions_keyboard(anime_id: int | str) -> InlineKeyboardMarkup:
    search_kb = InlineKeyboardMarkup(row_width=4)
    back = InlineKeyboardButton("⬅", callback_data=f"back.{anime_id}.search_edit_al")
    follow_btn = InlineKeyboardButton(
        "❤️ Подписаться", callback_data=f"follow.{anime_id}.search_edit_al"
    )
    mark_on_shiki = InlineKeyboardButton(
        "📌 Шикимори", callback_data=f"shikimori.{anime_id}.search_edit_al"
    )
    get_torrent = InlineKeyboardButton(
        "⬇ torrent", callback_data=f"torrent.{anime_id}.search_edit_al"
    )
    search_kb.add(back, follow_btn).add(mark_on_shiki).add(get_torrent)
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
        InlineKeyboardButton("⬅", callback_data=f"back.{anime_id}.shiki_mark_action"),
    ]
    kb.add(*buttons)
    return kb
