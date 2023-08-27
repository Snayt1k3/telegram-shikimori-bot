import logging

from aiogram import executor, types, Dispatcher
import asyncio
from bot import dp, anilibria_client, bot
from handlers.main import register_handlers
from anilibria import Connect

# Register handlers
register_handlers(dp)


async def set_default_commands(dp: Dispatcher) -> None:
    await dp.bot.set_my_commands(
        [
            types.BotCommand("about", "Информация о боте"),
            types.BotCommand("commands", "Меню со всеми доступными вам действиями"),
        ]
    )


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        f"Привет! Я ШикиАниме BOT\n" + f"Если хочешь использовать меня по полной, "
        f"тебе надо будет привязать свой профиль с Шикимори\n"
        f"Используй комманду - /profile",
    )


@anilibria_client.on(Connect)
async def on_connect(event: Connect):
    logging.info("Connected to Anilibria Api")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(anilibria_client.astart(), loop=loop)
    executor.start_polling(
        dp, skip_updates=True, on_startup=set_default_commands, loop=loop
    )
