import asyncio

from aiogram import executor, types

from Keyboard.reply import kb_profile
from bot import dp
from handlers.main import register_handlers
from websocket import ws_connect

# Register handlers
register_handlers(dp)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(f"Привет! Я ШикиАниме BOT\n" +
                        f"Если хочешь использовать меня по полной, "
                        f"тебе надо будет привязать свой профиль с Шикимори\n"
                        f"Нажми на кнопку - <b>😁 My Profile</b>",
                        reply_markup=kb_profile, parse_mode="HTML")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(ws_connect())
    executor.start_polling(dp, skip_updates=True, loop=loop)
