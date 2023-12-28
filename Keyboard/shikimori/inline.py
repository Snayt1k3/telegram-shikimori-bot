from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from database.dto.animes import ShikimoriAnime
from handlers.Shikimori.utils.shiki_api import shiki_api

user_lists_clk = CallbackData("user_lists", "anime_id", "status")

delete_from_list_clk = CallbackData("delete_from_list", "anime_id")

cancel_clk = CallbackData("cancel")

score_clk = CallbackData("score", "anime_id")

episode_start_clk = CallbackData("episode_start", "anime_id")
episode_clk = CallbackData("episode", "anime_id", "episode")
pagination_episode = CallbackData("episode_pagination", "anime_id", "page")

update_score_clk = CallbackData("shiki_score", "score", "anime_id")
update_score = CallbackData("update_score", "anime_id")

pagination_anime = CallbackData("pagination_anime", "collection", "page")

anime_view = CallbackData("anime_view", "anime_id", "collection")
anime_view_back = CallbackData("anime_view_back", "collection")

user_rate_view = CallbackData("user_rate_view", "anime_id", "collection")
pagination_user_rate = CallbackData("pagination_user_rate", "collection", "page")


async def episodes_keyboard(
    anime_id: str | int, episodes: int, page: int = 0
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=7)
    page = int(page)
    max_ep = episodes if episodes < page + 24 else page + 24

    kb.add(
        *[
            InlineKeyboardButton(
                f"{i}", callback_data=episode_clk.new(anime_id=anime_id, episode=i)
            )
            for i in range(page, max_ep)
        ]
    )

    btns = [
        InlineKeyboardButton(
            "<<",
            callback_data=pagination_episode.new(anime_id=anime_id, page=page - 24),
        ),
        InlineKeyboardButton(
            ">>",
            callback_data=pagination_episode.new(anime_id=anime_id, page=page + 24),
        ),
    ]

    if page > 0 and episodes > 24:
        kb.add(*btns)
    elif page == 0 and episodes > 24:
        kb.add(btns[1])
    elif episodes > 24:
        kb.add(btns[0])

    kb.add(InlineKeyboardButton("Удалить Сообщение ❌", callback_data=cancel_clk.new()))

    return kb


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

    kb.add(InlineKeyboardButton("Удалить Сообщение ❌", callback_data=cancel_clk.new()))
    return kb


async def keyboard_user_rate_view(
    animes: list[int], collection: str, page: int = 0
) -> InlineKeyboardMarkup:
    """
    Keyboard for user rates, when we use auth scope
    """
    kb = InlineKeyboardMarkup(row_width=3)
    page = int(page)
    animes_info = await shiki_api.get_animes_info(animes[page : page + 8])
    for anime in animes_info.text:
        kb.add(
            InlineKeyboardButton(
                anime["russian"],
                callback_data=user_rate_view.new(
                    anime_id=anime["id"], collection=collection
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

    kb.add(InlineKeyboardButton("Удалить Сообщение ❌", callback_data=cancel_clk.new()))

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
            "✏️ Оценка", callback_data=update_score.new(anime_id=anime_id)
        ),
        InlineKeyboardButton(
            "🗑 Удалить", callback_data=delete_from_list_clk.new(anime_id=anime_id)
        ),
        InlineKeyboardButton(
            "Отметить Эпизод",
            callback_data=episode_start_clk.new(anime_id=anime_id),
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
    kb.add(InlineKeyboardButton("Удалить Сообщение ❌", callback_data=cancel_clk.new()))
    return kb


async def shiki_keyboard(anime_id: str | int) -> InlineKeyboardMarkup:
    """
    keyboard when user edit one anime
    """
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = await all_actions_buttons(anime_id)
    kb.add(*buttons)
    kb.add(InlineKeyboardButton("Удалить Сообщение ❌", callback_data=cancel_clk.new()))
    return kb


async def shiki_user_rate_kb(anime_id: str | int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = await all_actions_buttons(anime_id)
    buttons.append(
        InlineKeyboardButton("Удалить Сообщение ❌", callback_data=cancel_clk.new())
    )
    kb.add(*buttons)
    return kb
