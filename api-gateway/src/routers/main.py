from fastapi import FastAPI
from src.routers.rates import router as rate_router
from src.routers.title import router as title_router
from src.routers.auth import router as auth_router
from src.routers.user import router as user_router


def include(app: FastAPI) -> None:
    app.include_router(rate_router)
    app.include_router(title_router)
    app.include_router(auth_router)
    app.include_router(user_router)
