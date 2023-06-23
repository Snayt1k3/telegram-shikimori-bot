from aiogram.dispatcher.filters.state import State, StatesGroup


class AnimeSearchState(StatesGroup):
    anime_str = State()


class UserNicknameState(StatesGroup):
    auth_code = State()


class AnimeMarkState(StatesGroup):
    anime_title = State()




