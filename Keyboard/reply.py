from aiogram.types import ReplyKeyboardMarkup

keyboard_status = ReplyKeyboardMarkup()
keyboard_status.add("completed", "watching").add("planned").add("rewatching", "dropped")

default_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard.add("/AnimeSearch", "/AnimeMark") \
    .add("/MyProfile", '/ResetProfile') \
    .add('/MyWatchList', '/MyPlannedList')
