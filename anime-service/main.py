import asyncio
import logging

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
    asyncio.run(main())
