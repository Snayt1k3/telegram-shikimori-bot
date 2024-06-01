from aiogram import types

from src.presentation.telegram.common.message import Message


async def send_about(message: types.Message):
    await message.reply(Message.about())


async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(Message.start())
