from aiogram.fsm.state import StatesGroup, State


class ShikimoriAuth(StatesGroup):
    code = State()


