from aiogram.fsm.state import StatesGroup, State

class SearchState(StatesGroup):
    query = State()
