from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


# profile callbacks
profile_manager = CallbackData("shikimori_profile", "action")
unlink_manager = CallbackData("shikimori_unlink", "action")


async def keyboard_unlink() -> InlineKeyboardMarkup:
    """unlink keyboard (True/False)"""
    kb = InlineKeyboardMarkup()
    btns = [
        InlineKeyboardButton("❌", callback_data=unlink_manager.new("no")),
        InlineKeyboardButton("✔️", callback_data=unlink_manager.new("yes")),
    ]
    kb.add(*btns)
    return kb


async def keyboard_profile() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    btns = [
        InlineKeyboardButton(
            "😐 UnLink Profile", callback_data=profile_manager.new("unlink")
        )
    ]
    kb.add(*btns)
    return kb


def cr_search_kb(anime_id):
    al_search_kb = InlineKeyboardMarkup(row_width=4)
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
    al_search_kb.add(back, follow_btn).add(mark_on_shiki).add(get_torrent)
    return al_search_kb


def cr_all_follows_kb(anime_id):
    anilibria_all_follows_kb = InlineKeyboardMarkup(row_width=4)
    back = InlineKeyboardButton("⬅", callback_data=f"back.{anime_id}.all_follows_edit")
    unfollow = InlineKeyboardButton(
        "💔", callback_data=f"unfollow.{anime_id}.all_follows_edit"
    )
    mark_on_shiki = InlineKeyboardButton(
        "📌 Шикимори", callback_data=f"shikimori.{anime_id}.all_follows_edit"
    )
    get_torrent = InlineKeyboardButton(
        "⬇ torrent", callback_data=f"torrent.{anime_id}.all_follows_edit"
    )
    anilibria_all_follows_kb.add(back, unfollow).add(mark_on_shiki, get_torrent)
    return anilibria_all_follows_kb


def Admin_kb():
    kb = InlineKeyboardMarkup()
    notify = InlineKeyboardButton(
        "Сделать уведомление",
        callback_data="notify.admin",
    )
    wishes = InlineKeyboardButton(
        "Пожелания, баги",
        callback_data="wishes.admin",
    )
    kb.add(notify).add(wishes)
    return kb
