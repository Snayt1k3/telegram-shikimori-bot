from aiogram.dispatcher.filters.state import State, StatesGroup


class UserNicknameState(StatesGroup):
    auth_code = State()


class AnimeMarkState(StatesGroup):
    anime_title = State()
