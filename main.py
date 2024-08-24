import asyncio
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

from aiogram import types

from bot import bot, dp
from src.adapters.database.common.db import async_session
from src.presentation.telegram.handlers.anime.router import include_anime_routers
from src.presentation.telegram.handlers.general.router import include_general_routers
from src.presentation.telegram.handlers.user.router import register_user_router
from src.presentation.telegram.ioc import IoC


async def main() -> None:
    include_anime_routers(dp)
    include_general_routers(dp)
    register_user_router(dp)
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command="about", description="Информация о боте"),
            types.BotCommand(
                command="profile", description="Информация о вашем профиле Shikimori"
            ),
            types.BotCommand(
                command="menu",
                description="Меню со всеми доступными вам действиями",
            ),
        ]
    )
    ioc = IoC(async_session)

    await dp.start_polling(bot, ioc=ioc)


if __name__ == "__main__":
    log_filename = "logs/shiki.log"
    handler = TimedRotatingFileHandler(
        log_filename, when="midnight", interval=1, backupCount=7
    )

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
