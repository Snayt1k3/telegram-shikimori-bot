from fastapi import FastAPI
from rate import rate_router
from title import title_router
from auth import auth_router


def include(app: FastAPI) -> None:
    app.include_router(rate_router)
    app.include_router(auth_router)
    app.include_router(title_router)
