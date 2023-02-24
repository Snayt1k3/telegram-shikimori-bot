from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

keyboard_status = ReplyKeyboardMarkup()
keyboard_status.add("completed").add("watching").add("planned").add("rewatching").add("dropped")


default_keyboard = ReplyKeyboardMarkup()
default_keyboard.add("/AnimeSearch").add("/AnimeMark")


keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_cancel.add('Cancel')