from fastapi import FastAPI
from rate import router as rate_router
from title import router as title_router

def include(app: FastAPI) -> None:
    app.include_router(rate_router)
    app.include_router(title_router)
