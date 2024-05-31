import asyncio
import logging
import sys

from aiogram import types
from src.presentation.telegram.handlers.general import general
from src.presentation.telegram.handlers.anime import anime_router
from src.presentation.telegram.handlers.notification import notify
from src.presentation.telegram.handlers.user import usr_router
from bot import bot, dp


async def main() -> None:
    dp.include_routers(general, usr_router, notify, anime_router)
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command="about", description="Информация о боте"),
            types.BotCommand(
                command="", description="Информация о вашем профиле Shikimori"
            ),
            types.BotCommand(
                command="commands",
                description="Меню со всеми доступными вам действиями",
            ),
        ]
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
