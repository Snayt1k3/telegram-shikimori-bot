import asyncio
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from bot import bot, dp
from src.adapters.http import HttpAdapter


async def main() -> None:
    setup_logging()
    # add_routers(dp)
    http_adapter = HttpAdapter()
    await dp.start_polling(bot, http_adapter=http_adapter)


def setup_logging() -> None:
    if not os.path.exists("logs"):
        os.mkdir("logs")

    log_filename = "logs/bot.log"
    handler = TimedRotatingFileHandler(
        log_filename, when="midnight", interval=1, backupCount=7
    )

    logging.basicConfig(level=logging.INFO, handlers=[handler])


if __name__ == "__main__":
    asyncio.run(main())
