import asyncio

from aiogram import executor, types, Dispatcher

from Keyboard.reply import kb_profile
from bot import dp
from handlers.main import register_handlers

# Register handlers
register_handlers(dp)


async def set_default_commands(dp: Dispatcher) -> None:
    await dp.bot.set_my_commands(
        [
            types.BotCommand("about", "Информация о боте"),
            types.BotCommand("commands", "Меню со всеми доступными вам действиями")
        ]
    )


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(f"Привет! Я ШикиАниме BOT\n" +
                        f"Если хочешь использовать меня по полной, "
                        f"тебе надо будет привязать свой профиль с Шикимори\n"
                        f"Нажми на кнопку - <b>😁 My Profile</b>",
                        reply_markup=kb_profile)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=True, loop=loop, on_startup=set_default_commands)
