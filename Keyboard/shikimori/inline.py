from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from database.dto.animes import ShikimoriAnime

user_lists_clk = CallbackData("user_lists", "anime_id", "status")
back_list_clk = CallbackData("back_shiki_list", "page", "status", "coll")

delete_from_list_clk = CallbackData("delete_from_list", "anime_id")

cancel_clk = CallbackData("cancel")

mark_episode_clk = CallbackData("episode_mark", "episode_action", "anime_id")
score_clk = CallbackData("score", "anime_id")

update_score_clk = CallbackData("shiki_score", "score", "anime_id")
update_score = CallbackData("update_score")

pagination_anime = CallbackData("pagination_anime", "collection", "page")

anime_view = CallbackData("anime_view", "anime_id", "collection")
anime_view_back = CallbackData("anime_view_back", "collection")

user_rate_view = CallbackData("user_rate_view", "anime_id")
pagination_user_rate = CallbackData("pagination_user_rate", "collection", "page")


async def keyboard_anime_view(
    animes: list[ShikimoriAnime], collection: str, page: int = 0
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    for anime in animes[page : page + 8]:
        kb.add(
            InlineKeyboardButton(
                anime.title_ru,
                callback_data=anime_view.new(anime_id=anime.id, collection=collection),
            )
        )

    btns = [
        InlineKeyboardButton(
            "<<",
            callback_data=pagination_anime.new(collection=collection, page=page - 8),
        ),
        InlineKeyboardButton(
            ">>",
            callback_data=pagination_anime.new(collection=collection, page=page + 8),
        ),
    ]

    if len(animes) > 8 and page > 0:
        kb.add(*btns)

    elif page > 0:
        kb.add(btns[0])

    elif len(animes) > 8:
        kb.add(btns[1])

    kb.add(InlineKeyboardButton("cancel ❌", callback_data=cancel_clk.new()))
    return kb


async def keyboard_user_rate_view(
    animes: list[ShikimoriAnime], collection: str, page: int = 0
) -> InlineKeyboardMarkup:
    """
    Keyboard for user rates, when we use auth scope
    """
    kb = InlineKeyboardMarkup()

    for anime in animes:
        kb.add(
            InlineKeyboardButton(
                anime.title_ru,
                callback_data=user_rate_view.new(
                    anime_id=anime.id, collection=collection
                ),
            )
        )

    btns = [
        InlineKeyboardButton(
            "<<",
            callback_data=pagination_user_rate.new(
                collection=collection, page=page - 8
            ),
        ),
        InlineKeyboardButton(
            ">>",
            callback_data=pagination_user_rate.new(
                collection=collection, page=page + 8
            ),
        ),
    ]

    if len(animes) > 8 and page > 0:
        kb.add(*btns)

    elif page > 0:
        kb.add(btns[0])

    elif len(animes) > 8:
        kb.add(btns[1])

    kb.add(InlineKeyboardButton("cancel ❌", callback_data=cancel_clk.new()))

    return kb


async def keyboard_by_coll(
    coll: str, target_id: int | str, page: int
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    back = InlineKeyboardButton("⬅", callback_data=back_list_clk.new(page=page))
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
                "-1 эпизод",
                callback_data=mark_episode_clk.new(
                    anime_id=target_id, episode_action="minus"
                ),
            ),
            InlineKeyboardButton(
                "+1 эпизод",
                callback_data=mark_episode_clk.new(
                    anime_id=target_id, episode_action="plus"
                ),
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


async def all_actions_buttons(anime_id: str | int) -> list[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            "✔️ Просмотрено",
            callback_data=user_lists_clk.new(anime_id=anime_id, status="completed"),
        ),
        InlineKeyboardButton(
            "🎥 Смотрю",
            callback_data=user_lists_clk.new(anime_id=anime_id, status="watching"),
        ),
        InlineKeyboardButton(
            "🗑 Брошено",
            callback_data=user_lists_clk.new(anime_id=anime_id, status="dropped"),
        ),
        InlineKeyboardButton(
            "📝 Запланированное",
            callback_data=user_lists_clk.new(anime_id=anime_id, status="planned"),
        ),
        InlineKeyboardButton(
            "✏️ Оценка", callback_data=score_clk.new(anime_id=anime_id)
        ),
        InlineKeyboardButton(
            "🗑 Удалить", callback_data=delete_from_list_clk.new(anime_id=anime_id)
        ),
    ]


async def score_keyboard(anime_id: int | str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=6)
    kb.add(
        *[
            InlineKeyboardButton(
                f"{i}", callback_data=update_score_clk.new(anime_id=anime_id, score=i)
            )
            for i in range(11)
        ]
    )
    return kb


async def shiki_keyboard(anime_id: str | int, collection: str) -> InlineKeyboardMarkup:
    """
    keyboard when user edit one anime
    """
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = await all_actions_buttons(anime_id)
    buttons.append(
        InlineKeyboardButton(
            "⬅ Назад", callback_data=anime_view_back.new(collection=collection)
        )
    )
    kb.add(*buttons)
    return kb


async def shiki_user_rate_kb(anime_id: str | int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = await all_actions_buttons(anime_id)
    buttons.append(InlineKeyboardButton("Cancel", callback_data=cancel_clk.new()))
    kb.add(*buttons)
    return kb
