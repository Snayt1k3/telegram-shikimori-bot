from fastapi import FastAPI
from src.routers.auth import router


def include_routers(app: FastAPI) -> None:
    app.include_router(router)
