from aiogram import Router
from aiogram.filters import Command, CommandStart

from src.presentation.telegram.common import Cancel
from .about import send_about, send_welcome
from .cancel import cancel
from .menu import send_menu

general_router = Router(name="general")

general_router.message.register(send_about, Command("about"))
general_router.message.register(send_welcome, CommandStart())
general_router.message.register(send_menu, Command("menu"))

general_router.callback_query.register(cancel, Cancel.filter())

