from aiogram import types
from aiogram.types import InlineKeyboardMarkup


async def edit_message_with_photo(msg: types.Message, photo: str, text: str, reply_markup: InlineKeyboardMarkup):
    await msg.edit_media(types.InputMediaPhoto(photo))
    await msg.edit_caption(text, reply_markup=reply_markup)


async def edit_message_with_file(msg: types.Message, file: str, text: str, reply_markup: InlineKeyboardMarkup):
    await msg.edit_media(types.InputMedia(open(file, "rb")))
    await msg.edit_caption(text, reply_markup=reply_markup)
