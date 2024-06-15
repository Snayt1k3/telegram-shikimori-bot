import asyncio
import logging
import sys

from aiogram import types

from bot import bot, dp
from src.presentation.telegram.handlers.anime.router import include_anime_routers
from src.presentation.telegram.handlers.general.router import include_general_routers

from src.presentation.telegram.handlers import notification
from src.presentation.telegram.handlers import user
from src.presentation.telegram.ioc import IoC
from src.adapters.database.common.db import async_session


async def main() -> None:
    include_anime_routers(dp)
    include_general_routers(dp)
    dp.include_routers(
        user.usr_router,
        notification.notify_router,
    )
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
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
