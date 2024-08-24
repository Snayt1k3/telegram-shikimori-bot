from aiogram import Dispatcher
from .follows import router as follows_router
from .auth import router as auth_router


def register_user_router(dp: Dispatcher) -> None:
    dp.include_routers(follows_router, auth_router)
