from aiogram import Dispatcher
from src.handlers.auth.main import router as auth_router
from src.handlers.profile.main import router as profile_router


def add_routers(dp: Dispatcher) -> None:
    dp.include_routers(auth_router, profile_router)
