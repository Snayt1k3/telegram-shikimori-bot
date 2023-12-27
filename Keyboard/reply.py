from aiogram.types import ReplyKeyboardMarkup


default_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard.add("🔍 Поиск").add("📝 Смотрю", "📝 Планирую", "📝 Просмотрено").add(
    "❤️ Подписки", "💘 Подписаться", "⬇ Торрент"
)
