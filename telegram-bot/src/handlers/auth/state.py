from aiogram.fsm.state import StatesGroup, State


class AuthState(StatesGroup):
    code = State()
