from aiogram.types import ReplyKeyboardMarkup


default_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard.add("📌 Mark").add(
    "📄 Watch List", "📄 Planned List", "📄 Completed List"
).add("❤️ Подписки", "💘 Подписаться", "⬇ Торрент")
