from aiogram import types
from aiogram.filters import CommandStart, Command

from src.presentation.telegram.common.message import Message
from src.presentation.telegram.handlers.general.router import general


@general.message(Command("about"))
async def about(message: types.Message):
    await message.reply(Message.about())


@general.messtaage(CommandStart())
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(Message.start())
