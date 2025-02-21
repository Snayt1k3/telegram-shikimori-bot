import asyncio
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from src.handlers.main import add_routers
from src.adapters.http import HttpAdapter
from src.adapters.auth import AuthAdapter
from aiogram import types

from bot import bot, dp


async def main() -> None:
    setup_logging()
    add_routers(dp)
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command="help", description="Информация о боте."),
            types.BotCommand(
                command="profile",
                description="Информация о вашем профиле Shikimori и не только.",
            ),
        ]
    )
    http_adapter = HttpAdapter()
    auth_adapter = AuthAdapter(http_adapter)
    await dp.start_polling(bot, http_adapter=http_adapter, auth_adapter=auth_adapter)


def setup_logging() -> None:
    if not os.path.exists("logs"):
        os.mkdir("logs")

    log_filename = "logs/ZeroShiki.log"
    handler = TimedRotatingFileHandler(
        log_filename, when="midnight", interval=1, backupCount=7
    )

    logging.basicConfig(level=logging.INFO, handlers=[handler])


if __name__ == "__main__":
    asyncio.run(main())
