import asyncio
import logging
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


if __name__ == "__main__":
    # Настраиваем логирование в файл
    log_handler = TimedRotatingFileHandler(
        "./logs/anime-service.log", when="midnight", interval=1
    )
    log_handler.suffix = "%Y-%m-%d"
    log_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)
    asyncio.run(main())
