import asyncio
import logging
import os
from logging.handlers import TimedRotatingFileHandler

import redis
from aiogram.fsm.storage.redis import RedisStorage

from bot import bot, dp
from src.adapters.http import HttpAdapter
from src.config.redis import redis_cfg


async def main() -> None:
    setup_logging()
    # add_routers(dp)
    http_adapter = HttpAdapter()
    dp.storage = RedisStorage(redis=redis.from_url(redis_cfg.url))
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
