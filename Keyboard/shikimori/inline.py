from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from database.schemas.animes import ShikimoriAnime


planned_list_clk = CallbackData("planned_list", "anime_id")
completed_list_clk = CallbackData("completed_list", "anime_id")
dropped_list_clk = CallbackData("dropped_list", "anime_id")
watching_list_clk = CallbackData("watching_list", "anime_id")
back_list_clk = CallbackData("back_shiki_list", "page")

delete_from_list_clk = CallbackData("delete_from_list", "anime_id")

cancel_clk = CallbackData("cancel")

mark_episode_clk = CallbackData("episode_mark", "episode_action", "anime_id")
score_clk = CallbackData("score", "anime_id")

update_score_clk = CallbackData("shiki_score", "score", "anime_id")

pagination_clk = CallbackData("pagination", "collection", "page")

anime_mark_back = CallbackData("anime_mark_back")

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


async def keyboard_by_coll(coll: str, target_id: int | str, page: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    back = InlineKeyboardButton(
        "⬅", callback_data=back_list_clk.new(page=page)
    )
    update_rating = InlineKeyboardButton(
        "✏️ Оценка", callback_data=score_clk.new(anime=target_id)
    )
    delete = InlineKeyboardButton(
        "🗑 Удалить", callback_data=delete_from_list_clk.new(anime_id=target_id)
    )

    kb.add(back, update_rating)

    if coll == "anime_watching":
        kb.add(
            InlineKeyboardButton(
                "-1 эпизод", callback_data=mark_episode_clk.new(anime_id=target_id, episode_action="minus")
            ),
            InlineKeyboardButton(
                "+1 эпизод", callback_data=mark_episode_clk.new(anime_id=target_id, episode_action="minus")
            ),
        )

        kb.add(
            InlineKeyboardButton(
                "✔️ Просмотрено",
                callback_data=completed_list_clk.new(anime_id=target_id),
            ),
            InlineKeyboardButton(
                "🗑 Брошено", callback_data=dropped_list_clk.new(anime_id=target_id)
            ),
        )

    elif coll == "anime_planned":
        kb.add(
            InlineKeyboardButton(
                "✔️ Просмотрено",
                callback_data=completed_list_clk.new(anime_id=target_id),
            ),
            InlineKeyboardButton(
                "🎥 Смотрю", callback_data=watching_list_clk.new(anime_id=target_id)
            ),
        )

    kb.add(delete)
    return kb


async def all_actions_buttons(anime_id) -> list[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            "✔️ Просмотрено", callback_data=completed_list_clk.new(anime_id=anime_id)
        ),
        InlineKeyboardButton(
            "🎥 Смотрю", callback_data=watching_list_clk.new(anime_id=anime_id)
        ),
        InlineKeyboardButton(
            "🗑 Брошено", callback_data=dropped_list_clk.new(anime_id=anime_id)
        ),
        InlineKeyboardButton(
            "📝 Запланированное", callback_data=planned_list_clk.new(anime_id=anime_id)
        ),
        InlineKeyboardButton(
            "✏️ Оценка", callback_data=score_clk.new(anime_id=anime_id)
        ),
        InlineKeyboardButton(
            "🗑 Удалить", callback_data=delete_from_list_clk
        )
    ]


async def shiki_mark_keyboard(anime_id):
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = await all_actions_buttons(anime_id)
    buttons.append(
        InlineKeyboardButton("⬅ Назад", callback_data=anime_mark_back.new())
    )
    kb.add(*buttons)
    return kb
