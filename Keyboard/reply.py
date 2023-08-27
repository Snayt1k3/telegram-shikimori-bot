from aiogram.types import ReplyKeyboardMarkup

keyboard_status = ReplyKeyboardMarkup()
keyboard_status.add("completed", "watching").add("planned").add("rewatching", "dropped")

default_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard.add("📌 Mark").add("😁 Profile", "😐 UnLink Profile").add(
    "📄 Watch List", "📄 Planned List", "📄 Completed List"
).add("❤️ Follows", "💘 Follow to Anime", "⬇ torrent")
