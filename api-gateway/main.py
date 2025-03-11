import logging
import os
from logging.handlers import TimedRotatingFileHandler

import uvicorn
from fastapi import FastAPI
from src.routers.main import include

app = FastAPI()
include(app)


def setup_logging() -> None:
    if not os.path.exists("logs"):
        os.mkdir("logs")

    log_filename = "logs/api-gateway.log"
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
    setup_logging()
    uvicorn.run(app, port=8001)
