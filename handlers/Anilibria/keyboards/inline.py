from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def all_follows_kb(follows, action=None, page=0):
    match action:
        case "-":
            page -= 8
        case "+":
            page += 8

    kb = InlineKeyboardMarkup()

    for anime in follows[page : page + 8]:
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
