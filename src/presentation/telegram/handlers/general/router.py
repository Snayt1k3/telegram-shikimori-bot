from aiogram import Dispatcher

from .about import router as about_router
from .cancel import router as cancel_router
from .menu import router as menu_router


def include_general_routers(dp: Dispatcher):
    dp.include_routers(cancel_router, menu_router, about_router)