import asyncio
import logging
import sys

from aiogram import types

from bot import bot, dp
from src.presentation.telegram.handlers import anime
from src.presentation.telegram.handlers import general
from src.presentation.telegram.handlers import notification
from src.presentation.telegram.handlers import user


async def main() -> None:
    dp.include_routers(general.general_router, user.usr_router, anime.anime_router, notification.notify_router)
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command="about", description="Информация о боте"),
            types.BotCommand(
                command="profile", description="Информация о вашем профиле Shikimori"
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
