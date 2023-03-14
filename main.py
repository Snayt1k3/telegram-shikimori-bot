from aiogram import executor, types
from Keyboard.reply import default_keyboard
from bot import dp
from handlers.main import register_handlers
from handlers.translator import set_lang_code, translate_text
# Handlers Register
register_handlers(dp)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await set_lang_code(message)
    await message.reply(f"{await translate_text(message, 'Hi i am ShikiAnime')} BOT\n" +
                        f"{await translate_text(message, 'if you wanna use all my functional')},\n"
                        f"{await translate_text(message, 'Call The command')} - <b>/MyProfile</b>",
                        reply_markup=default_keyboard, parse_mode="HTML")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
