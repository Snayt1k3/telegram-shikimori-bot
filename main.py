from aiogram import executor, types
from Keyboard.keyboard import default_keyboard
from bot import *
from handlers import shikimori_handlers

# Configure logging
logging.basicConfig(level=logging.INFO)

# Handlers Register
shikimori_handlers.register_handlers(dp)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi i'm ShikiAnime bot", reply_markup=default_keyboard)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
