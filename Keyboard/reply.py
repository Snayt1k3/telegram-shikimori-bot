from aiogram.types import ReplyKeyboardMarkup

keyboard_status = ReplyKeyboardMarkup()
keyboard_status.add("completed", "watching").add("planned").add("rewatching", "dropped")

default_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard.add("🔍 Anime Search", "🖊 Anime Mark") \
    .add("😁 My Profile", '😐 Reset Profile') \
    .add('📽 My Watch List', '📃 My Planned List', '☑ My Completed List') \
    .add('❤ My Follows', '💌 Follow to Anime', '⬇ Get torrent')
