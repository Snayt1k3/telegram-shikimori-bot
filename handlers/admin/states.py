from aiogram.dispatcher.filters.state import State, StatesGroup


class NotifyState(StatesGroup):
    text = State()
