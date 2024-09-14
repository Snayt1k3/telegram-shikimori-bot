from aiogram import types, Router
from aiogram.filters import Command, CommandStart

from src.presentation.telegram.common.message import Message

router = Router(name="about")


@router.message(Command("about"))
async def send_about(message: types.Message, messages: Message):
    await message.reply(messages.about)


@router.message(CommandStart())
async def send_welcome(message: types.Message, messages: Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(messages.start)
