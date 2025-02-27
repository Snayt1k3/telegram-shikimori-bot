import asyncio
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from src.handlers.main import start_receiving_messages

logger = logging.getLogger(__name__)


async def main():
    logger.info("Application started")
    try:
        await start_receiving_messages()

    except KeyboardInterrupt:
        logger.info("Application stopped")

    except Exception as e:
        logger.error(f"Application crashed: {str(e)}")


def setup_logging() -> None:
    if not os.path.exists("logs"):
        os.mkdir("logs")

    log_filename = "logs/anime-service.log"
    handler = TimedRotatingFileHandler(
        log_filename, when="midnight", interval=1, backupCount=7
    )
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        " [in %(pathname)s:%(lineno)d]"
    )
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[handler])


if __name__ == "__main__":
    # Настраиваем логирование в файл
    setup_logging()
    asyncio.run(main())
