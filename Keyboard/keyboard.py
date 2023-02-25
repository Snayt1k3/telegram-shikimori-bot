from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

keyboard_status = ReplyKeyboardMarkup()
keyboard_status.add("completed", "watching").add("planned").add("rewatching", "dropped")


default_keyboard = ReplyKeyboardMarkup()
default_keyboard.add("/AnimeSearch").add("/AnimeMark")


keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_cancel.add('Cancel')


inline_kb_tf = InlineKeyboardMarkup()
no_btn = InlineKeyboardButton("No", callback_data="reset_user.False")
yes_btn = InlineKeyboardButton("Yes", callback_data="reset_user.True")
inline_kb_tf.add(yes_btn, no_btn)
