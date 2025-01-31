from fastapi import FastAPI
from src.routers.rate import rate_router
from src.routers.title import title_router
from src.routers.auth import auth_router


def include(app: FastAPI) -> None:
    app.include_router(rate_router)
    app.include_router(auth_router)
    app.include_router(title_router)
