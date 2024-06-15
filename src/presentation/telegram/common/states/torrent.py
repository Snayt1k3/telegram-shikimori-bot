from aiogram.fsm.state import StatesGroup, State

class TorrentState(StatesGroup):
    query = State()
