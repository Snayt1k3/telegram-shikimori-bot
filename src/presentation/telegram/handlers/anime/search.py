from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from src.application.enums import ShikimoriEntryType
from src.presentation.telegram.common import Message
from src.presentation.telegram.common.enums import SearchEngineEnum
from src.presentation.telegram.common.keyboards import SearchCallback, search_keyboard
from src.presentation.telegram.common.states import SearchState
from src.presentation.telegram.interactor_factory import InteractorFactory

router = Router(name="search")


@router.message(F.text == "Поиск")
async def start_search(msg: types.Message):
    """
    Requesting from user about platform he wants to search anime
    """
    text = Message.search_start_message()
    kb = search_keyboard()
    await msg.answer(text=text, reply_markup=kb)


@router.callback_query(SearchCallback.filter())
async def search_set_query(
    call: types.CallbackQuery, state: FSMContext, callback_data: SearchCallback
):
    """
    Starting getting date for query
    """
    await state.set_state(SearchState.query)
    await state.update_data(engine=str(callback_data.engine))
    await call.message.answer(Message.search_query_message())


@router.message(SearchState.query)
async def search(msg: types.Message, state: FSMContext, ioc: InteractorFactory):
    await state.clear()

    data = await state.get_data()
    engine = data.get("engine")

    if engine == SearchEngineEnum.shikimori:
        res = await search_on_shikimori(msg.text, ioc)

    else:
        res = await search_on_anilibria(msg.text, ioc)

    # todo добавить отрисовку и пагинацию


async def search_on_shikimori(query: str, ioc: InteractorFactory):

    async with ioc.shikimori_search() as usecase:
        res = await usecase(query, ShikimoriEntryType.ANIME)

    return res


async def search_on_anilibria(query: str, ioc: InteractorFactory):

    async with ioc.anilibria_search() as usecase:
        res = await usecase(query)

    return res
