from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.schemas.animes import AnilibriaAnime


async def all_follows_kb(follows, action=None, page=0):
    match action:
        case "-":
            page -= 8
        case "+":
            page += 8

    kb = InlineKeyboardMarkup()

    for anime in follows[page: page + 8]:
        kb.add(
            InlineKeyboardButton(
                anime.title_ru, callback_data=f"view.{anime.id}.all_follows"
            )
        )

    # add pagination buttons response by current page
    if len(follows) > page + 8 and page > 0:
        kb.add(
            InlineKeyboardButton(text="<<", callback_data=f"prev.{page}.all_follows"),
            InlineKeyboardButton(text=">>", callback_data=f"next.{page}.all_follows"),
        )

    elif len(follows) > page + 8:
        kb.add(
            InlineKeyboardButton(text=">>", callback_data=f"next.{page}.all_follows"),
        )

    elif page > 0:
        kb.add(
            InlineKeyboardButton(text="<<", callback_data=f"prev.{page}.all_follows")
        )

    return kb


async def search_anime_kb(animes: list[AnilibriaAnime]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    for anime in animes:
        kb.add(
            InlineKeyboardButton(anime.title_ru, callback_data=f"{anime.id}.search_al")
        )

    kb.add(InlineKeyboardButton("❌ Cancel", callback_data=f"cancel.search_al"))
    return kb


async def animes_from_shikimori_kb(animes: list[dict]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    for anime in animes:
        kb.add(
            InlineKeyboardButton(
                anime["russian"], callback_data=f"view.{anime['id']}.shikimori_founds"
            )
        )
    kb.add(InlineKeyboardButton("❌ Cancel", callback_data=f"cancel.shikimori_founds"))
    return kb
