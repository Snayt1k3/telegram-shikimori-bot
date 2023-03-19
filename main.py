from aiogram import executor, types, Dispatcher
from Keyboard.reply import kb_profile
from bot import dp
from handlers.main import register_handlers
from handlers.translator import set_lang_code, translate_text
from websocket import ws_connect
import asyncio


# Register handlers
register_handlers(dp)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await set_lang_code(message)
    await message.reply(f"{await translate_text(message, 'Hi i am ShikiAnime')} BOT\n" +
                        f"{await translate_text(message, 'if you wanna use all my functional')},\n"
                        f"{await translate_text(message, 'Click on button')} - <b>😁 My Profile</b>",
                        reply_markup=kb_profile, parse_mode="HTML")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(ws_connect())

    executor.start_polling(dp, skip_updates=True, loop=loop)

