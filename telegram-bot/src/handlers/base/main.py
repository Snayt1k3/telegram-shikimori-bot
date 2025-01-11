from aiogram import Router, types
from aiogram.filters import Command, CommandStart

router = Router(name="BaseCommands")


@router.message(CommandStart())
async def start_handler(m: types.Message) -> None:
    pass


@router.message(Command("help"))
async def help_handler(m: types.Message) -> None:
    pass
