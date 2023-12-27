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
