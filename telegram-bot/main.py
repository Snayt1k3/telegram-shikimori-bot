import asyncio
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

from aiogram import types

from bot import bot, dp


async def main() -> None:

    await bot.set_my_commands(
        commands=[
            types.BotCommand(command="help", description="Информация о боте."),
            types.BotCommand(
                command="profile",
                description="Информация о вашем профиле Shikimori и не только.",
            ),
        ]
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    log_filename = "logs/ZeroShiki.log"
    handler = TimedRotatingFileHandler(
        log_filename, when="midnight", interval=1, backupCount=7
    )

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
